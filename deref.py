import json

import click
import jsonref


@click.command()
@click.argument('input_yaml')
@click.argument('output_json')
def cli(input_yaml, output_json):
    """Convert a openapi yaml specification to json without $ref references"""
    with open(input_yaml, 'r') as fin:
        api = json.load(fin)

    api_noref = jsonref.JsonRef.replace_refs(api)
    with open(output_json, 'w') as fout:
        json.dump(api_noref, fout, indent=4)


if __name__ == '__main__':
    cli()
