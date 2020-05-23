from dataclasses import dataclass, InitVar
from typing import Iterable, Dict
from pathlib import Path
from os import path
import logging


@dataclass
class CommonParams:
    """
        Base class with common parameters.

        Attributes
        ----------
        dry_run : int
            if true, final output is printed and not written to ouptut file
        verbose : int
            enables detailed logs
        input_file : str
            absolute file path to read from
        output_file : str
            absolute file path to write to
        file_type : str
            extension of file used to determine how to read the input file

        Methods
        -------
        No methods implemented.
    """

    dry_run: int
    verbose: int
    input_file: Path = None
    output_file: Path = None
    file_type: str = None

    def __post_init__(self):
        level = logging.DEBUG if self.verbose else logging.INFO
        logging.basicConfig(format="%(asctime)s - %(message)s", level=level)
        logging.info(
            f'Starting file parser for {self.input_file}. {"DRY RUN" if  self.dry_run else ""}'
        )


@dataclass
class FileParams:
    """
        FileParams takes in relative paths for input file and output file.
        Determines whether the user passed in a directory or a single file.

        Attributes
        ----------
        file_path : InitVar[int]
            Temporary input,can be a directory or a file path, used to build the absolute path called built_file_name
        output_path : int
            Can be a directory or a file path, dependent on input file name to build  built_output_path
        built_file_name : str
            absolute file path to read from
        output_type : Path
            extension of file used to determine how to write the output file
        file_type : str
            extension of file used to determine how to read the input file
        p : Path
            Path object used to determine whether file_path is a directory or a file

        Methods
        -------
        build_output_path(file_name)
        returns absolute output path by using the input file name, built output path and  file extension

        get_file()
        yield a dictionary containing input and output file paths
    """

    file_path: InitVar[str]
    output_path: str
    built_file_name: str = None
    output_type: Path = None
    file_type: str = None
    p: Path = None

    def __post_init__(self, file_path: str):
        """
            Parameters
            ----------
            file_path : str
                input file path
        """
        self.p = Path(file_path)
        if self.p.is_dir():
            if not self.file_type:
                raise ValueError
            self.built_file_name = f"*.{self.file_type}"
        else:
            self.built_file_name = self.p.name
            self.p = self.p.parent

    def build_output_path(self, input_file: Path) -> str:
        """
            Parameters
            ----------
            input_file : Path
                name of the input file to build absolute output path
        """
        output_file_path = Path(self.output_path)
        file_name = path.splitext(input_file.name)[0]
        if output_file_path.is_dir():
            output_file_path = output_file_path / f"{file_name}.{self.output_type}"
        return output_file_path.resolve()

    def get_file_path(self) -> Iterable[Dict]:
        for input_file in self.p.glob(self.built_file_name):
            output_file = self.build_output_path(input_file)
            yield dict(input_file=input_file, output_file=output_file)
