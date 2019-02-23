import json

import click
import jsonref


@click.command()
@click.argument('input_json', type=click.File(mode='r'))
@click.argument('output_json', type=click.File(mode='w'))
def cli(input_json, output_json):
    """Convert a openapi yaml specification to json without $ref references"""

    # Due to https://github.com/OpenAPITools/openapi-generator/issues/2172
    # we need to resolve references on the properties used for the pagination
    # envelopes. However, we must not change all other references because it
    # makes the generator create many inline_response objects.
    # Here, we find all references and keep only those referring to pagination
    # parameters
    whitelist = (
        '#/components/schemas/PaginationEnvelope/properties/page',
        '#/components/schemas/PaginationEnvelope/properties/pages',
        '#/components/schemas/PaginationEnvelope/properties/total',
    )
    api_noref = unref(jsonref.load(input_json), whitelist)
    json.dump(api_noref, output_json, indent=4)


def unref(obj, whitelist):
    """ Unreference JsonRef objects in `obj` when not present in `whitelist`."""
    if isinstance(obj, jsonref.JsonRef):
        if obj.__reference__['$ref'] not in whitelist:
            obj = obj.__reference__
    elif isinstance(obj, dict):
        for key in obj:
            obj[key] = unref(obj[key], whitelist)
    elif isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = unref(obj[i], whitelist)
    return obj


if __name__ == '__main__':
    cli()
