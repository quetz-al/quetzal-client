import functools
import traceback

import click

from quetzal.client import Client,Configuration


class State(object):

    def __init__(self):
        self.api_config = Configuration()
        self.api_client = Client(self.api_config)
        self.verbose_level = 0


# Decorator to obtain the state directly. Use with @pass_state
pass_state = click.make_pass_decorator(State, ensure=True)


class FamilyVersionType(click.ParamType):
    name = 'family version'

    def convert(self, value, param, ctx):
        parts = value.split(':')
        if len(parts) != 2:
            self.fail(f'"{value}" is an invalid family-version definition. '
                      f'It must be family_name:version_number.',
                      param, ctx)
        family = parts[0]
        if parts[1] == 'latest':
            version = None
        else:
            version = click.types.IntRange(0).convert(parts[1], param, ctx)

        return family, version

    def __repr__(self):
        return f'FamilyVersion()'


class FamilyVersionListType(FamilyVersionType):
    name = 'family version list'

    def convert(self, value, param, ctx):
        parts = value.split(',')
        definitions = []
        for p in parts:
            tup = FamilyVersionType.convert(self, p, param, ctx)
            definitions.append(tup)
        return definitions


class BaseGroup(click.Group):
    """A group whose `no_args_is_help` option is our custom help function"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse_args(self, ctx, args):
        if not args and self.no_args_is_help and not ctx.resilient_parsing:
            _format_help(ctx)
        return super().parse_args(ctx, args)


def _collect_options(cmd, ctx, list_help=True):
    opts = []
    for param in cmd.get_params(ctx):
        if not list_help and param.name in ('help', 'help_all'):
            continue
        rv = param.get_help_record(ctx)
        if rv is not None:
            opts.append(rv)
    return opts


def _format_options(cmd, ctx, formatter, list_help=True):
    """Writes all the options into the formatter if they exist."""
    opts = _collect_options(cmd, ctx, list_help)

    if opts:
        if cmd.options_metavar:
            title = cmd.options_metavar.replace('[', '').replace(']', '')
        else:
            title = 'Options'
        with formatter.section(title):
            formatter.write_dl(opts)


def _format_help(ctx):
    # We are going to need to do some operations on the parent contexts, but
    # traversing this by .parent gives a reversed result
    parent_contexts = []
    current = ctx.parent
    while current is not None:
        parent_contexts.append(current)
        current = current.parent
    parent_contexts = parent_contexts[::-1]

    formatter = ctx.make_formatter()

    # Obtain the correct usage considering the options of parent commands
    pieces = []
    for parent in parent_contexts:
        parent_pieces = parent.command.collect_usage_pieces(parent)
        # Change 'COMMAND [ARGS]...' with the instantiation of the command
        parent_pieces[1] = parent.info_name
        # Remove '[OPTIONS]' if there are none
        has_options = bool(_collect_options(parent.command, parent, list_help=False))
        if not has_options:
            parent_pieces.pop(0)
        pieces.extend(parent_pieces[::-1])
    pieces.append(ctx.info_name)
    pieces.extend(ctx.command.collect_usage_pieces(ctx))
    prog = pieces[0]
    args = pieces[1:]
    formatter.write_usage(prog, ' '.join(args))

    # Add the help_text of the current command
    ctx.command.format_help_text(ctx, formatter)

    # Add the options of parent command but not their sub-commands
    for parent in parent_contexts:
        _format_options(parent.command, parent, formatter, list_help=False)

    # Add the options of this command
    _format_options(ctx.command, ctx, formatter, list_help=True)
    # ...and its available sub-commands if it is a MultiCommand
    if isinstance(ctx.command, click.MultiCommand):
        ctx.command.format_commands(ctx, formatter)

    # Finally, the epilog of this command
    ctx.command.format_epilog(ctx, formatter)

    # Show the message
    help_text = formatter.getvalue().rstrip('\n')
    click.echo(help_text, color=ctx.color)
    ctx.exit()


def all_help_option(f):
    def callback(ctx, param, value):
        if value and not ctx.resilient_parsing:
            _format_help(ctx)

    return click.option('--help-all',
                        help='Show a detailed help message with all options and exit.',
                        is_eager=True, expose_value=False, is_flag=True,
                        callback=callback)(f)


def help_options(f):
    f = click.help_option(help='Show help message for this command and exit.')(f)
    f = all_help_option(f)
    return f


def error_wrapper(f):
    """Decorator to gracely catch errors, show a messsage and exit."""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except click.ClickException:
            # Don't show the message, let click handle it
            raise
        except Exception as ex:
            ctx = click.get_current_context()
            click.secho(f'Operation failed: {type(ex).__name__}: {ex}.', fg='red')
            state = ctx.ensure_object(State)
            if state.verbose_level > 0:
                click.echo(ex)
                traceback.print_exc()
            ctx.exit(code=-1)

    return wrapper


def rename_kwargs(**replacements):
    def actual_decorator(func):
        @functools.wraps(func)
        def decorated_func(*args, **kwargs):
            for internal_arg, external_arg in replacements.items():
                if external_arg in kwargs:
                    kwargs[internal_arg] = kwargs.pop(external_arg)
            return func(*args, **kwargs)
        return decorated_func
    return actual_decorator


class MutexOption(click.Option):
    def __init__(self, *args, **kwargs):
        self.not_required_if = kwargs.pop('not_required_if')

        assert self.not_required_if, '"not_required_if" parameter required'
        kwargs['help'] = (
            kwargs.get('help', '') +
            ' Option is mutually exclusive with ' +
            ', '.join(self.not_required_if) + '.'
        ).strip()
        super().__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        if not ctx.resilient_parsing:
            current_opt = self.name in opts
            for mutex_opt in self.not_required_if:
                if mutex_opt in opts:
                    if current_opt:
                        raise click.UsageError(f'Illegal usage: {self.name} is '
                                               f'mutually exclusive with {mutex_opt}.')
                    else:
                        self.prompt = None
        return super().handle_parse_result(ctx, opts, args)


class OneRequiredOption(click.Option):
    """Like MutexOption, but needs exactly one of the required options"""

    def __init__(self, *args, **kwargs):
        self.one_of_with = kwargs.pop('one_of_with')

        assert self.one_of_with, '"one_of_with" parameter required'
        kwargs['help'] = (
                kwargs.get('help', '') +
                ' Option is mutually exclusive with ' +
                ', '.join(self.one_of_with) + ', but at most ' +
                'one of these options is required.'
        ).strip()
        super().__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        if not ctx.resilient_parsing:
            current_opt = self.name in opts
            num_present = current_opt + sum(other in opts for other in self.one_of_with)
            if num_present == 0:
                raise click.UsageError('Illegal usage: one of the options ' +
                                       ", ".join([self.name] + self.one_of_with) +
                                       ' is required.')

            # Keep this loop like MutexOption to identify which other parameter is in conflict with this one
            for mutex_opt in self.one_of_with:
                if mutex_opt in opts:
                    if current_opt:
                        raise click.UsageError(f'Illegal usage: {self.name} is '
                                               f'mutually exclusive with {mutex_opt}.')
                    else:
                        self.prompt = None
        return super().handle_parse_result(ctx, opts, args)
