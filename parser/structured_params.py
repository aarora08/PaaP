from parser.utils import (
    apply_lambda, date_to_str, create_column, set_columns, drop_columns, add_to_pipe, write_to_json,
    write_iterrow_to_json,
)
from pandas import DataFrame, read_csv, read_excel, read_json
from parser.common_params import CommonParams
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any
from datetime import datetime
from hashlib import md5
import logging


@dataclass
class BasePandasParams(CommonParams):
    """
       Base class for all pandas related classes, extends CommonParams to inherit common attributes

       Attributes
       ----------
       df : DataFrame
           pandas dataframe object
       available_read_type : Dict
           contains available pandas read functions

       Methods
       -------
        get_df()
            utilizes available read types to determine which pandas read function to use
        write_json()
            writes the dataframe to json
        inject_data(action)
            utility method to inject all attributes of the class object, and inject the dataframe
            where action is a dictionary
        parse():
            iterates over each action in the pipeline and calls add to pipe utility function
            once all operations from the pipeline have been applied, the method write_json is called
   """

    df: DataFrame = None
    available_read_types: Dict = field(
        default_factory=dict(
            csv=read_csv, xls=read_excel, xlsx=read_excel, json=read_json
        )
    )
    write_to_file: Any = field(default_factory=write_to_json)

    def __post_init__(self):
        self.df = self.get_df()

    def get_df(self) -> DataFrame:
        logging.debug(f" Pandas file reader: reading file type {self.file_type}")
        df_reader = self.available_read_types[self.file_type]
        return df_reader(self.input_file)

    def inject_data(self, action: Dict) -> Dict:
        action["data_attr"] = self.__dict__[action["data_attr"]]
        action["df"] = self.df
        return action

    def parse(self):
        for action in self.pipeline:
            logging.debug(f' Running action {action["data_attr"]} for {self.input_file}')
            action = self.inject_data(action)
            self.df = add_to_pipe(**action)
        logging.debug(f"All actions completed for {self.input_file}")
        self.df = self.df.fillna("")
        if not self.dry_run:
            logging.debug(f" Writing {self.input_file} to file {self.output_file}")
            self.write_to_file(self.df, self.output_file)
        else:
            logging.info(self.df)


@dataclass
class TypeAParser(BasePandasParams):
    """
        Type A Parser Pipeline that contains one attribute per dataframe operation to be applied.
        Each attribute should be a list a dictionaries
        Each class that extends BasePandasParams should contain a pipeline attribute.
        No methods should be implemented in this class.
        Attributes
        ----------
        generic_actions: List[Dict]:
            contains dataframe information and actions to apply to it.
        pipeline: List[Dict]:
            flow of actions to apply to the dataframe
    """

    built_columns: List = field(
        default_factory=[dict(columns=["id", "Name", "sourceDate", "content"])]
    )
    columns_to_remove: List[Dict] = field(
        default_factory=[
            dict(columns=["No", "Description", "Task Description"]),
        ]
    )
    add_columns: List[Dict] = field(
        default_factory=[
            dict(column_name="generatedDate", column_value=datetime.now()),
            dict(column_name="type", column_value="Type A"),
            dict(column_name="category", column_value="public"),
            dict(column_name="contentLanguage", column_value="en"),
            dict(column_name="status", column_value="Full Time"),
        ]
    )
    dates_to_parse: List[Dict] = field(
        default_factory=[
            dict(column_name="generatedDate", format_str="%Y-%m-%d"),
            dict(column_name="sourceDate", format_str="%Y-%m-%d"),
        ]
    )
    lambdas_to_apply: List[Dict] = field(
        default_factory=[
            dict(
                apply_to_column="Name",
                set_to_column="Name",
                apply_with=lambda x: " ".join(x.strip().split(", ")[::-1]),
            ),
            dict(
                apply_to_column="content",
                set_to_column="content",
                apply_with=lambda x: [x],
            ),
            dict(
                apply_to_column="Name",
                set_to_column="id",
                apply_with=lambda s: md5(str.encode(s)).hexdigest(),
            ),
        ]
    )
    pipeline: List[Dict] = field(
        default_factory=[
            dict(fn=drop_columns, data_attr="columns_to_remove"),
            dict(fn=set_columns, data_attr="built_columns"),
            dict(fn=create_column, data_attr="add_columns"),
            dict(fn=date_to_str, data_attr="dates_to_parse"),
            dict(fn=apply_lambda, data_attr="lambdas_to_apply"),
        ]
    )


@dataclass
class TypeBParser(BasePandasParams):
    """
        Type B Parser that contains one attribute per dataframe operation to be applied.
        Each attribute should be a list a dictionaries
        Each class that extends BasePandasParams should contain a pipeline attribute.
        No methods should be implemented in this class.
        Attributes
        ----------
        generic_actions: List[Dict]:
            contains dataframe information and actions to apply to it.
        pipeline: List[Dict]:
            flow of actions to apply to the dataframe
    """

    columns_to_remove: List[Dict] = field(
        default_factory=[dict(columns=["Project Number", "Project Title"]),]
    )
    built_columns: List = field(
        default_factory=[dict(columns=["sourceDate", "Name", "content"])]
    )
    add_columns: List[Dict] = field(
        default_factory=[
            dict(column_name="generatedDate", column_value=datetime.now()),
            dict(column_name="type", column_value="Type B"),
            dict(column_name="category", column_value="public"),
            dict(column_name="contentLanguage", column_value="en"),
            dict(column_name="status", column_value="Full Time"),
        ]
    )
    dates_to_parse: List[Dict] = field(
        default_factory=[
            dict(column_name="generatedDate", format_str="%Y-%m-%d"),
            dict(column_name="sourceDate", format_str="%Y-%m-%d"),
        ]
    )
    lambdas_to_apply: List[Tuple] = field(
        default_factory=[
            dict(
                apply_to_column="Name",
                set_to_column="Name",
                apply_with=lambda x: " ".join(x.strip().split(", ")[::-1]),
            ),
            dict(
                apply_to_column="content",
                set_to_column="content",
                apply_with=lambda x: [x],
            ),
            dict(
                apply_to_column="Name",
                set_to_column="id",
                apply_with=lambda s: md5(str.encode(s)).hexdigest(),
            ),
        ]
    )
    pipeline: List[Dict] = field(
        default_factory=[
            dict(fn=drop_columns, data_attr="columns_to_remove"),
            dict(fn=set_columns, data_attr="built_columns"),
            dict(fn=create_column, data_attr="add_columns"),
            dict(fn=date_to_str, data_attr="dates_to_parse"),
            dict(fn=apply_lambda, data_attr="lambdas_to_apply"),
        ]
    )


@dataclass
class TypeCParser(BasePandasParams):
    """
        Type C Parser that contains one attribute per dataframe operation to be applied.
        Each attribute should be a list a dictionaries
        Each class that extends BasePandasParams should contain a pipeline attribute.
        No methods should be implemented in this class.
        Attributes
        ----------
        generic_actions: List[Dict]:
            contains dataframe information and actions to apply to it.
        pipeline: List[Dict]:
            flow of actions to apply to the dataframe
    """

    columns_to_remove: List[Dict] = field(
        default_factory=[dict(columns=(["Title"])),]
    )
    built_columns: List = field(
        default_factory=[
            dict(
                columns=[
                    "fullName",
                    "id",
                    "email",
                    "persSubArea",
                    "persArea",
                    "dept",
                ]
            )
        ]
    )
    columns_to_add: List[Dict] = field(
        default_factory=[
            dict(column_name="generatedDate", column_value=datetime.now()),
            dict(column_name="type", column_value="Type C"),
            dict(column_name="category", column_value="public"),
            dict(column_name="contentLanguage", column_value="en"),
            dict(column_name="status", column_value="Full Time"),
        ]
    )
    dates_to_parse: List[Dict] = field(
        default_factory=[dict(column_name="generatedDate", format_str="%Y-%m-%d"),]
    )
    lambdas_to_apply: List[Tuple] = field(
        default_factory=[
            dict(
                apply_to_column="fullName",
                set_to_column="fullName",
                apply_with=lambda x: " ".join(x.strip().split(", ")[::-1]),
            ),
            dict(
                apply_to_column="fullName",
                set_to_column="id",
                apply_with=lambda s: md5(str.encode(s)).hexdigest(),
            ),
        ]
    )
    pipeline: List[Dict] = field(
        default_factory=[
            dict(fn=drop_columns, data_attr="columns_to_remove"),
            dict(fn=set_columns, data_attr="built_columns"),
            dict(fn=create_column, data_attr="columns_to_add"),
            dict(fn=date_to_str, data_attr="dates_to_parse"),
            dict(fn=apply_lambda, data_attr="lambdas_to_apply"),
        ]
    )
    write_to_file: Any = field(default_factory=write_iterrow_to_json)
