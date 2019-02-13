import click

import quetzal.client
from quetzal.client.cli import help_options, pass_state, State
from quetzal.client.cli.auth import auth
from quetzal.client.cli.data import data


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
        current_opt = self.name in opts
        for mutex_opt in self.not_required_if:
            if mutex_opt in opts:
                if current_opt:
                    raise click.UsageError(f'Illegal usage: {self.name} is '
                                           f'mutually exclusive with {mutex_opt}.')
                else:
                    self.prompt = None
        return super().handle_parse_result(ctx, opts, args)


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Quetzal client version x.y.z')
    ctx.exit()


def url_option(f):

    def callback(ctx, param, value):
        if value and not ctx.resilient_parsing:
            state = ctx.ensure_object(State)
            # Set or leave the default configuration value
            state.api_config.host = value or state.api_config.host

    return click.option('--url',
                        envvar='QUETZAL_URL',
                        help='Quetzal URL. If not set, uses environment '
                             'variable QUETZAL_URL.',
                        callback=callback)(f)


def user_option(f):

    def callback(ctx, param, value):
        if value and not ctx.resilient_parsing:
            state = ctx.ensure_object(State)
            state.api_config.username = value

    return click.option('--username',
                        envvar='QUETZAL_USER',
                        help='Quetzal username. If not set, uses environment '
                             'variable QUETZAL_USER.',
                        cls=MutexOption,
                        not_required_if=['token'],
                        callback=callback)(f)


def password_option(f):

    def callback(ctx, param, value):
        if value and not ctx.resilient_parsing:
            state = ctx.ensure_object(State)
            state.api_config.password = value

    return click.option('--password',
                        envvar='QUETZAL_PASSWORD',
                        help='Quetzal password. If not set, uses environment '
                             'variable QUETZAL_PASSWORD.',
                        cls=MutexOption,
                        not_required_if=['token'],
                        callback=callback)(f)


def token_option(f):

    def callback(ctx, param, value):
        if value and not ctx.resilient_parsing:
            state = ctx.ensure_object(State)
            state.api_config.access_token = value

    return click.option('--token',
                        envvar='QUETZAL_TOKEN',
                        help='Quetzal access token. If not set, uses environment '
                             'variable QUETZAL_TOKEN.',
                        cls=MutexOption,
                        not_required_if=['username', 'password'],
                        callback=callback)(f)


def verbose_option(f):
    def callback(ctx, param, value):
        if value and not ctx.resilient_parsing:
            state = ctx.ensure_object(State)
            state.api_config.debug = (value > 1)

    return click.option('-v', '--verbose', count=True, help='Verbosity level.',
                        expose_value=False,
                        callback=callback)(f)


def global_options(f):
    # Note that options need to be chained in reversed order
    f = click.version_option(version=quetzal.client.__version__)(f)
    f = help_options(f)
    f = verbose_option(f)
    f = token_option(f)
    f = password_option(f)
    f = user_option(f)
    f = url_option(f)
    return f


@click.group(options_metavar='[GLOBAL OPTIONS]')
@global_options
def cli(**kwargs):
    pass


cli.add_command(auth)
cli.add_command(data)



if __name__ == '__main__':
    cli()
