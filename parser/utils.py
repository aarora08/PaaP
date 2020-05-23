from xml.etree.ElementTree import XML
from dataclasses import _MISSING_TYPE
from typing import Any, List, Dict
from argparse import Namespace
from pandas import DataFrame
from zipfile import ZipFile
from pathlib import Path
import logging
import json


def apply_lambda(df: DataFrame, apply_with: str, apply_to_column: str = None, set_to_column: str = None) -> DataFrame:
    logging.debug(f"Applying lambda fn to df at: {apply_to_column}")
    df[set_to_column] = df[apply_to_column].apply(apply_with)
    return df


def create_column(df: DataFrame, column_name: str, column_value: str) -> DataFrame:
    logging.debug(
        f"Adding new column to df at: {column_name} with value: {column_value}"
    )
    df[column_name] = column_value
    return df


def drop_columns(df: DataFrame, columns: str, axis: int = 1) -> DataFrame:
    logging.debug(f"removing columns to df at: {columns}")
    df = df.drop(columns=columns, axis=axis)
    return df


def set_columns(df: DataFrame, columns: List) -> DataFrame:
    logging.debug(f"Set columns to df at: {columns}")
    df.columns = columns
    return df


def date_to_str(df: DataFrame, column_name: str, format_str: str) -> DataFrame:
    logging.debug(f"Date formatting in df at: {column_name}, with format: {format_str}")
    df[column_name] = df[column_name].dt.strftime(format_str)
    return df


def add_to_pipe(df: DataFrame, fn: Any, data_attr: List[Dict]) -> DataFrame:
    for item in data_attr:
        df = df.pipe(fn, **item)
    return df


def write_to_json(df: DataFrame, output_path: Path):
    df.to_json(output_path)


def write_iterrow_to_json(df: DataFrame, output_path: Path):
    built_json = []
    for column, row in df.iterrows():
        built_json.append(row.to_dict())
    with open(output_path, "w") as f:
        data = json.dumps(built_json)
        f.write(data)


def parse_docx(file_path: Path) -> str:
    """
    NOTE:
        http://xmlstackoverflow.blogspot.com/2014/09/reading-doc-extension-file-elementtree.html
        All microsoft files are zipped xml documents.
    """
    WORD_NAMESPACE = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    PARA = WORD_NAMESPACE + "p"
    TEXT = WORD_NAMESPACE + "t"

    with ZipFile(file_path) as document:
        try:
            xml_content = document.read("word/document.xml")
        except Exception as e:
            print(f"FAILED:{document}")
            logging.error(f"Failed to parsed document {file_path}", e)
            return
    tree = XML(xml_content)

    paragraphs = []
    for paragraph in tree.getiterator(PARA):
        texts = [
            node.text.replace("\xa0", " ").strip("  ")
            for node in paragraph.getiterator(TEXT)
            if node.text
        ]
        if texts:
            paragraphs.append("".join(texts))
    return " ".join(paragraphs)


def namespace_to_data_class(args: Namespace, tuple_type, additional=None) -> Any:
    """
    Automagically determine the arguments for a given dataclass and return an instantiated object.

    Parameters
    ----------
    args
    tuple_type
    additional

    Returns
    -------

    """
    data = dict()
    for field_name, field_obj in tuple_type.__dataclass_fields__.items():
        if type(field_obj.default_factory) != _MISSING_TYPE:
            data[field_name] = field_obj.default_factory
        else:
            data[field_name] = getattr(args, field_name, None)
    if additional:
        for key, value in additional.items():
            data[key] = value
    return tuple_type(**data)
