from parser.common_params import CommonParams
from dataclasses import dataclass, field
from parser.utils import parse_docx
from datetime import datetime
from typing import Dict
from hashlib import md5
import logging
import json


@dataclass
class CommonUnstructuredParams(CommonParams):
    """
       Base class for all unstructured data parsing related classes, extends CommonParams to inherit common attributes

       Attributes
       ----------
       data : Dict
           a base template dictionary to be used by child classes to build final json document
       content : Dict
           attribute to store the parsed content from a file

       Methods
       -------
        parse():
            base parse function that adds a timestamp, and adds content
        write_json()
            writes the dictionary to json

   """

    data: Dict = field(
        default_factory={
            "type": "doc",
            "sourceType": "proposal",
            "source": "company",
            "category": "public",
            "sourceDate": "2019-07-21",
            "location": "united states",
            "contentLanguage": "en",
            "status": "Full Time",
        }
    )
    content: str = None
    source_type: str = None

    def parse(self):

        logging.debug(f"Parsing Document for {self.input_file}")
        self.data["generatedDate"] = datetime.now().strftime("%Y-%m-%d")
        self.data["content"] = self.content
        self.data["type"] = self.source_type
        if not self.dry_run:
            self.write_json()
        else:
            logging.info(self.data)

    def write_json(self):
        logging.debug(f"Writing to file {self.output_file}")
        data_json = json.dumps([self.data])
        with open(self.output_file, "w") as f:
            f.write(data_json)


@dataclass
class UnstructuredParser(CommonUnstructuredParams):
    """
        Template Class for unstructured parser

        Methods
       -------
        parse():
            determines file type, calls utility function to read docx, reads txt files directly
    """

    def parse(self):
        if self.file_type in {"docx", "doc"}:
            self.content = parse_docx(self.input_file)
        elif self.file_type == "txt":
            with open(self.input_file, "r") as f:
                data = f.read()
            self.content = data
        self.source_type = self.file_type
        super().parse()


@dataclass
class TypeDParser(CommonUnstructuredParams):
    """
        Template Class for Type D
        Attributes:
        ---------
        id:
            id that is supposed to be a hash of name
        Methods
       -------
        parse():
            reads json files
            adds id to the id attribute
            calls parent parse method to write to file
        """

    def parse(self):
        with open(self.input_file, "r") as f:
            data = json.load(f)
        self.content = [data["type_d_text"].replace("\n", " ").strip()]
        print(self.content)
        self.data["id"] = md5(str.encode(data["name"])).hexdigest()
        self.source_type = "type_d"
        super().parse()
