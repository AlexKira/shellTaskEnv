# -*- coding: utf-8 -*-
import os
import json
from typing import Dict
from typing import List
from typing import Union


class BaseSchema(object):
    """
    Class contains a description of the settings \
        fields for managing the application.
    """

    __SCHEMA__ = {
        "CONFPATH": "/opt/shellTaskEnv/settings/conf.json",
        "TASK": {
            "0": {
                "DATE_TIME": {
                    "MONTH": str(),
                    "DAYS": str(),
                    "HOURS": str(),
                    "MINUTE": str()
                },
                "EXECUTE": {
                    "SHELL": list()
                },
            },
        },
        "LOGROTATION": {
            "LOGFILE": "/opt/shellTaskEnv/log/shellLogEnvApp.log",
            "ARCH": {
                "ENABLE": bool(),
                "DATE_TIME": {
                    "MONTH": str(),
                    "DAYS": str(),
                    "HOURS": str(),
                    "MINUTE": str()
                },
                "NAME": "shellLogEnvApp",
                "TYPE": "gz",  # zip | gz
                "DIR": "/opt/shellTaskEnv/log/arch",
                "TRUNCATE": True
            },
            "DELETE": {
                "ENABLE": bool(),
                "DAYS": 30
            },
        },
        "CONFDUMP": {
            "ENABLE": bool(),
            "DIR": "/opt/shellTaskEnv/dump/copy_conf.json"
        }
    }


class BaseExportSchema(BaseSchema):
    """Сlass for creating a schema and setting attributes."""

    CONFPATH: str = None
    TASK: Dict[
        str, Dict[
            str, Union[
                Dict[str, str],
                Dict[str, List[str]]
            ]
        ]
    ] = None
    LOGROTATION: Dict[
        str, Union[
            Dict[str, str],
            Dict[
                str, Union[
                    bool,
                    Dict[str, str],
                    str
                ]
            ],
            Dict[str, Union[bool, int]]
        ]
    ] = None
    CONFDUMP: Dict[str, Union[bool, str]] = None

    @classmethod
    def add_file_json(
        cls,
        path: str
    ) -> None:
        """
        Method for adding a configuration file in JSON format.
        ------------------------------------------------------
        :type path: str
        :param path: path to the configuration file.
        """
        subdir = os.path.dirname(path)
        if not os.path.isdir(subdir):
            os.makedirs(subdir)
        if not os.path.isfile(path):
            with open(path, "w") as file:
                json.dump(cls.__SCHEMA__, file, indent=4)

    @classmethod
    def load_from_file(
        cls,
        path: str
    ) -> None:
        """
        Method for opening a file and setting json schema attributes.
        -------------------------------------------------------------
        :type path: str
        :param path: path to the configuration file.
        """
        with open(path, "r") as schema:
            data = json.load(schema)
            for key, value in data.items():
                setattr(cls, key, value)

    def __init__(
        self,
        confPath: str = None
    ) -> None:
        """
        BaseExportSchema constructor object to get the json schema.
        -----------------------------------------------------------
        args:
            confPath: str - path to the configuration file. \
                If no value is passed, the default \
                    BaseSchema path object is used
        """
        try:
            if confPath is None:
                confPath = self.__SCHEMA__["CONFPATH"]
            else:
                self.__SCHEMA__["CONFPATH"] = confPath

            self.add_file_json(confPath)
            self.load_from_file(confPath)
        except json.decoder.JSONDecodeError as err:
            raise TypeError(
                f"Error in conf.json. ({err})"
            )
        except IsADirectoryError:
            raise IsADirectoryError(
                "Error. Check the directory and name of the transferred file."
            )
