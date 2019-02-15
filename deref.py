import json

import click
import jsonref


@click.command()
@click.argument('input_json', type=click.File(mode='r'))
@click.argument('output_json', type=click.File(mode='w'))
def cli(input_json, output_json):
    """Convert a openapi yaml specification to json without $ref references"""
    api = json.load(input_json)

    api_noref = jsonref.JsonRef.replace_refs(api)
    json.dump(api_noref, output_json, indent=4)


if __name__ == '__main__':
    cli()
