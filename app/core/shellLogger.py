# -*- coding: utf-8 -*-
import os
import time
import logging


class Logger:
    """Class for configuring the logger."""

    @classmethod
    def get(
        cls,
        pathfile: str,
        formatt: str,
        level: str = "INFO",
        getlogger: str = "cloudEnv",
        console: bool = False
    ) -> logging:
        """
        Method to get logger object.
        --------------------
        @returns: object logger.
        """
        formatter = logging.Formatter(
            fmt=formatt
        )
        if console:
            logging.basicConfig(
                level=level,
                format=formatt
            )
        logging.Formatter.converter = time.localtime
        logger = logging.getLogger(getlogger)
        logger.setLevel(level=level)
        loggerFile = logging.FileHandler(pathfile)
        loggerFile.setFormatter(formatter)
        logger.addHandler(loggerFile)
        return logger

    def __init__(
        self,
        pathfile: str,
        formatt: str,
        level: str = "INFO",
        getlogger: str = "shellTaskEnv",
        console: bool = False
    ) -> None:
        """
        Logger constructor object to set parameters.
        --------------------------------------------
        args:
            pathfile: str - log file path.
            formatt: str - stream output display format in log.
            level: str - default error levels "INFO".
            getlogger: int - get default logger name "shellTaskEnv".
            console: bool - output stream to the console.
        """
        check_subdir = os.path.dirname(pathfile)
        if not os.path.isdir(check_subdir):
            os.makedirs(check_subdir)
        self.get = self.get(pathfile, formatt, level, getlogger, console)
