from parser.structured_params import TypeAParser, TypeBParser, TypeCParser
from parser.unstructured_params import TypeDParser, UnstructuredParser
from parser.utils import namespace_to_data_class
from argparse import ArgumentParser, Namespace
from parser.common_params import FileParams
import logging


def build_parser(description: str = None) -> ArgumentParser:
    parser = ArgumentParser(description)
    parser.add_argument("--verbose", action="count", default=0)
    parser.add_argument("--dry-run", action="count", default=0)

    common_parser = ArgumentParser(add_help=False)
    common_parser.add_argument("--file-path", required=True)
    common_parser.add_argument("--output-path", required=True)
    # TODO: Implement write to csv, txt
    common_parser.add_argument("--output-type", default="json", choices=["json", "csv"])
    # TODO: Implement read pdf
    common_parser.add_argument(
        "--file-type",
        default="xlsx",
        choices=["json", "xlsx", "xls", "doc", "docx", "csv", "txt"],
        required=False,
    )

    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    subparsers.add_parser("type_a", parents=[common_parser])
    subparsers.add_parser("type_b", parents=[common_parser])
    subparsers.add_parser("type_c", parents=[common_parser])
    subparsers.add_parser("type_d", parents=[common_parser])
    subparsers.add_parser("unstructured", parents=[common_parser])

    return parser


def main():
    parser: ArgumentParser = build_parser()
    args: Namespace = parser.parse_args()
    commands = dict(
        type_a=TypeAParser, type_b=TypeBParser, type_c=TypeDParser, type_d=TypeDParser, unstructured=UnstructuredParser,
    )
    action = commands[args.command]
    file_params = namespace_to_data_class(args, FileParams)
    for built_file_params in file_params.get_file_path():
        parser_built = namespace_to_data_class(args, action, additional=built_file_params)
        logging.info(f'parsing file: {built_file_params["input_file"]}')
        parser_built.parse()
        logging.info(f'saved to: {built_file_params["output_file"]}')
