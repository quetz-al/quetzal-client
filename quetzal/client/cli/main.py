import logging

import click

from quetzal.client import Client, Configuration
from quetzal.client.cli import BaseGroup, help_options, State, MutexOption
from quetzal.client.cli.auth import auth_group
from quetzal.client.cli.file import file_group
from quetzal.client.cli.query import query_command
from quetzal.client.cli.workspace import workspace_group


logger = logging.getLogger(__name__)


def url_option(f):

    def callback(ctx, param, value):
        if value and not ctx.resilient_parsing:
            state = ctx.ensure_object(State)
            # Set or leave the default configuration value
            state.api_config.host = value or state.api_config.host

    default_value = Configuration().host
    return click.option('--url',
                        envvar='QUETZAL_URL',
                        default=default_value,
                        show_default=True,
                        help='Quetzal URL. If not set, uses environment '
                             'variable QUETZAL_URL if this variable is defined.',
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
                        not_required_if=['token', 'api_key'],
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
                        not_required_if=['token', 'api_key'],
                        callback=callback)(f)


def token_option(f):

    def callback(ctx, param, value):
        if value and not ctx.resilient_parsing:
            state = ctx.ensure_object(State)
            state.api_config.access_token = value

    return click.option('--token',
                        envvar='QUETZAL_TOKEN',
                        help='Quetzal bearer token. If not set, uses environment '
                             'variable QUETZAL_TOKEN.',
                        cls=MutexOption,
                        not_required_if=['username', 'password', 'api_key'],
                        callback=callback)(f)


def apikey_option(f):

    def callback(ctx, param, value):
        if value and not ctx.resilient_parsing:
            state = ctx.ensure_object(State)
            state.api_config.api_key['X-API-KEY'] = value

    return click.option('--api-key',
                        envvar='QUETZAL_API_KEY',
                        help='Quetzal API key. If not set, uses environment '
                             'variable QUETZAL_API_KEY',
                        cls=MutexOption,
                        not_required_if=['username', 'password', 'token'],
                        callback=callback)(f)


def insecure_option(f):

    def callback(ctx, param, value):
        if value and not ctx.resilient_parsing:
            state = ctx.ensure_object(State)
            state.api_config.verify_ssl = False
            # Changing the verify_ssl option needs propagation in the client
            state.api_client = Client(state.api_config)
            # Mute urllib3 warnings
            import urllib3
            urllib3.disable_warnings()

    return click.option('--insecure',
                        is_flag=True,
                        help='Do not verify HTTPS certificates.',
                        callback=callback)(f)


def verbose_option(f):

    def callback(ctx, param, value):
        if value and not ctx.resilient_parsing:
            state = ctx.ensure_object(State)
            state.api_config.debug = (value > 1)
            state.verbose_level = value

    return click.option('-v', '--verbose', count=True,
                        help='Verbosity level. Use -v for verbose, '
                             '-vv for even more verbosity',
                        expose_value=False,
                        callback=callback)(f)


def global_options(f):
    import quetzal.client
    import quetzal.openapi_client
    version_str = f'{quetzal.client.__version__} '\
        f'(openapi_client version: {quetzal.openapi_client.__version__}) ' \
        f'(generator version: {quetzal.openapi_client.__openapi_generator_cli_version__})'

    # Note that options need to be chained in the reversed order
    # (with respect to how parameters are captured on the command functions)
    f = click.version_option(version=version_str)(f)
    f = help_options(f)
    f = verbose_option(f)
    f = insecure_option(f)
    f = apikey_option(f)
    f = token_option(f)
    f = password_option(f)
    f = user_option(f)
    f = url_option(f)
    return f


@click.group(options_metavar='[GLOBAL OPTIONS]', cls=BaseGroup)
@global_options
def cli(*args, **kwargs):
    """Command-line utility for the Quetzal API client."""
    logger.debug('Global options: %s %s', args, kwargs)


cli.add_command(auth_group)
cli.add_command(file_group)
cli.add_command(query_command)
cli.add_command(workspace_group)


if __name__ == '__main__':
    cli()
