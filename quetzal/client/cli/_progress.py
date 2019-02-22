# -*- coding: utf-8 -*-
import functools
import itertools

import click

_PROGRESS_CHARS = '⠇⡆⣄⣠⢰⠸⠙⠋⠇⡇⣇⣧⣷⣾⣽⣻⢿⡿⣟⣯⣷⣯⣟⡿⢿⣻⣽⣾⣷⣧⣇⡇⠇⠋⠙⠸⢰⣠⣄⡆'


def generic_progress(end_message='', func=None, clear=None):
    return dict(
        func=func or _generic_message,
        kwargs=dict(char_iterator=itertools.cycle(_PROGRESS_CHARS)),
        clear=clear or functools.partial(_generic_clear, end_message)
    )


def commit_progress():

    def custom_clear(w_details, *args, **kwargs):
        if w_details.status == 'READY':
            message = 'Workspace commit successful.'
        else:
            message = 'Workspace commit failed.'
        _clear_and_message(message)

    return generic_progress(clear=custom_clear)


def scan_progress():

    def custom_clear(w_details, *args, **kwargs):
        if w_details.status == 'READY':
            message = 'Workspace scan successful.'
        else:
            message = 'Workspace scan failed.'
        _clear_and_message(message)

    return generic_progress(clear=custom_clear)


def _generic_clear(message, *args, **kwargs):
    term_width, _ = click.get_terminal_size()
    extra_width = term_width - len(message)  # Count how many whitespaces needed to clear the line
    click.secho('\r' + str(message) + (' ' * extra_width), nl=True, fg='green')


def _generic_message(w_details, char_iterator=None):
    click.echo(f'\rWaiting for workspace {w_details.id} {w_details.name} '
               f'[{w_details.status}] ... {next(char_iterator) if char_iterator else ""}',
               nl=False)


def _clear_and_message(message):
    term_width, _ = click.get_terminal_size()
    extra_width = term_width - len(message)  # Count how many whitespaces needed to clear the line
    click.secho('\r' + str(message) + (' ' * extra_width), nl=True, fg='green')
