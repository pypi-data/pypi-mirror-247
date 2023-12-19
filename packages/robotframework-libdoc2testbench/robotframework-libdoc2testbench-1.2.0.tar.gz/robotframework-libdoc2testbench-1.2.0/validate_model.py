import argparse
import re
import sys
from pathlib import Path

from lxml import etree


def download_schema(schema_url):
    try:
        import requests
    except ImportError as err:
        raise ImportError(
            "If a schema from URL should be used, install Python 'requests' first."
        ) from err
    try:
        response = requests.get(schema_url)
        response.raise_for_status()
        return response.content
    except Exception as e:
        raise Exception(f"Failed to download schema: {e}") from e


def validate(xml_file, xsd_file=None):
    tree = etree.parse(xml_file)

    if xsd_file:
        schema_tree = etree.parse(xsd_file)
    else:
        schema_location = tree.getroot().get(
            '{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation'
        )
        if not schema_location:
            raise Exception("No schema location found in XML and no XSD file provided.")
        schema_content = download_schema(schema_location)
        schema_tree = etree.fromstring(schema_content)

    schema = etree.XMLSchema(schema_tree)

    try:
        schema.assertValid(tree)
        print("XML is valid against the schema.")
    except etree.DocumentInvalid as e:
        print("XML is invalid!")
        for error in e.error_log:
            escaped_file = re.escape(xml_file)
            line_match = re.search(f"{escaped_file}:(\\d+):", str(error))
            if line_match:
                print(f"Line: {Path(xml_file).resolve()}:{line_match.group(1)}")
                short_error = re.sub(f"{escaped_file}:(\\d+):", "", str(error))
                print(f"    Error: {short_error}")
                continue
            print(f"Error: {error}")
        sys.exit(len(e.error_log))


def main():
    parser = argparse.ArgumentParser(description="XML Validator Tool")
    parser.add_argument("xml_file", type=str, help="Path to the XML file to be validated")
    parser.add_argument(
        "--xsd",
        type=str,
        help="Path to an optional XSD file. If provided,"
        " this schema is used instead of the one specified in the XML file.",
    )

    args = parser.parse_args()

    try:
        validate(args.xml_file, args.xsd)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
