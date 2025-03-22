# -*- coding: utf-8 -*-
import os
import re
import time
import signal
from typing import Generator
from core.queue import DictQueue
from core.shellLogger import Logger
from core.schema import BaseExportSchema
from core.chron import (
    AddPlanTask,
    AddIntervalTask
)
from core.handlers import (
    CopyConfDump,
    DeleteLogArch,
    LogArch,
    TruncateLogFile
)


QUEUE = DictQueue()


def getLogger(
    pathfile: str = None,
    console: bool = False,
    name: str = "shellTaskEnv"
) -> Logger:
    """
    Function to get Logger object.
    ------------------------------
    :type pathfile: str
    :param pathfile: log file path.

    :type console: bool
    :param console: output stream to the console.

    :type name: str
    :param name: get default logger name "shellTaskEnv".

    :rtype: object
    :returns: Logger().get.
    """
    if pathfile is None:
        pathfile = (
            BaseExportSchema.__SCHEMA__["LOGROTATION"]["LOGFILE"]
        )
    logger = Logger(
        pathfile=pathfile,
        formatt=(
            "[%(asctime)s.%(msecs)d]"
            "[%(name)s]"
            "[%(levelname)s]"
            "[%(process)d]"
            "[%(threadName)s]"
            "[%(thread)d]"
            "[%(filename)s]"
            "[%(funcName)s]:\n"
            "%(message)s"
        ),
        getlogger=name,
        console=console,
    ).get
    return logger


def initCfg() -> BaseExportSchema:
    """
    Function for initializing and checking the configuration file.
    """
    rootCfg = BaseExportSchema.__SCHEMA__["CONFPATH"]
    obj = BaseExportSchema()
    if obj.CONFPATH != rootCfg:
        obj = BaseExportSchema(obj.CONFPATH)
    check_cfg = {
        key: val
        for key, val in BaseExportSchema.__dict__.items()
        if val is None
    }
    status = None in check_cfg.values()
    if status:
        raise KeyError(check_cfg)
    return obj


def __formattingTypes(
    data: dict = BaseExportSchema.TASK
) -> tuple[None | int | float]:
    """
    Function to convert parameters for datetime.
    --------------------------------------------
    :type data: dict
    :param data: object BaseExportSchema.TASK

    :rtype: tuple
    :returns: None | int | float.
    """
    if not isinstance(data, dict):
        raise TypeError(
            "Invalid parameter type 'data'."
            "May be 'dict'"
        )
    isKeys = {
        data.get("MONTH", False),
        data.get("DAYS", False),
        data.get("HOURS", False),
        data.get("MINUTE", False)
    }
    if False in isKeys:
        raise KeyError(data)

    mo = d = h = mi = None
    isInt: bool = lambda string: string.isdigit()
    values = [
        (
            re.sub(r"[/*, !@#$%?]", "", x)
        ) for x in data.values()
    ]
    mo, d, h, mi = [
        x if x.strip() else None for x in values
    ]
    # Check month
    if mo is not None:
        if isInt(mo):
            mo = int(mo)
        else:
            mo = float(mo)
    # Check day
    if d is not None:
        if isInt(d):
            d = int(d)
        else:
            d = float(d)
    # Check hour
    if h is not None:
        if isInt(h):
            h = int(h)
        else:
            h = float(h)
    # Check minute
    if mi is not None:
        if isInt(mi):
            # add minutes
            mi = int(mi)
        else:
            # add seconds
            mi = float(mi)
    return mo, d, h, mi


def __calcDTime(
    data: dict = BaseExportSchema.TASK
) -> tuple:
    """
    Function for calculating task completion time.
    ----------------------------------------------
    :type data: dict
    :param data: object BaseExportSchema.TASK

    :rtype: tuple
    :returns: (
        datetime(year, month, day, hour, minute, second),
        datetime(year, month, day, hour, minute).timestamp(),
        str
    )
    """
    dt = tstamp = dtype = None
    dTime = __formattingTypes(data)
    if (
        "/" in "".join(data.values()) or
        any(isinstance(x, float) for x in dTime)
    ):
        mo, d, h, mi = dTime
        call = AddIntervalTask(
            month=mo,
            day=d,
            hour=h,
            minute=mi
        )
        dt = call.current_datetime()
        tstamp = dt.timestamp()
        dtype = "IntervalTask"
    elif (
        "*" in "".join(data.values()) or
        any(isinstance(x, int) for x in dTime)
    ):
        mo, d, h, mi = dTime
        call = AddPlanTask(
            month=mo,
            day=d,
            hour=h,
            minute=mi
        )
        dt = call.current_datetime()
        tstamp = dt.timestamp()
        dtype = "PlanTask"
    return dt, tstamp, dtype


def logShellRotationTask(
    logger: Logger,
    data: dict = BaseExportSchema.LOGROTATION
) -> None:
    """
    Function for working with logfiles rotation.
    --------------------------------------------
    :type logger: object
    :param logger: getLogger() function reference.

    :type data: dict
    :param data: object BaseExportSchema.LOGROTATION.
    """
    archName = data["ARCH"]["NAME"]
    fromDir = os.path.dirname(data["LOGFILE"])
    toDir = data["ARCH"]["DIR"]
    typeArch = data["ARCH"]["TYPE"]
    truncate = data["ARCH"]["TRUNCATE"]
    call = LogArch(
        archName=archName,
        fromDir=fromDir,
        toDir=toDir,
        typeArch=typeArch
    )
    logger.info(
        f"Archive added: {call.out}"
    )
    call = TruncateLogFile(
        truncate=truncate,
        abspath_filename=data["LOGFILE"]
    )
    if call.out is not None:
        logger.info(
            f"Logfile truncated: {call.out}"
        )
    if data["DELETE"]["ENABLE"]:
        enable = data["DELETE"]["ENABLE"]
        count_days = data["DELETE"]["DAYS"]
        call = DeleteLogArch(
            enable=enable,
            dirpath=toDir,
            days=count_days
        )
        out = call.out
        if len(out) > 0:
            logger.info(
                f"Archive deleted: {out}"
            )


def addShellTask(
    data: dict = BaseExportSchema.TASK
) -> None:
    """
    Function of adding tasks to queue.
    ----------------------------------
    :type data: dict
    :param data: object BaseExportSchema.TASK.
    """
    if data is None:
        raise KeyError(
            "Error. Configuration file data was not transferred. "
            f"Result: {data}"
        )

    for key, val in data.items():
        dt, tstamp, dtype = __calcDTime(val["DATE_TIME"])
        if "" not in val["DATE_TIME"].values():
            QUEUE.add(
                key=key,
                value={
                    "DATE_TIME": str(dt),
                    "TIMESTAMP": tstamp,
                    "TYPE": dtype,
                    "SHELL": val["EXECUTE"]["SHELL"],
                }
            )


def updateShellTask(
    worktime: time,
    data: dict = BaseExportSchema.TASK,
) -> Generator[None, str, None]:
    """
    Function for updating tasks in the queue.
    -----------------------------------------
    :type worktime: time
    :param worktime: links to current timestamp.

    :type data: dict
    :param data: object BaseExportSchema.TASK.

    :rtype: Generator
    :returns: None | str.
    """
    if data is None:
        raise KeyError(
            "Error. Configuration file data was not transferred. "
            f"Result: {data}"
        )
    for key, val in QUEUE.get().items():
        if worktime >= val["TIMESTAMP"]:
            if key == "LOGROTATION":
                dt, tstamp, dtype = __calcDTime(
                    val["CONF_DATA"]["ARCH"]["DATE_TIME"]
                )
                QUEUE.update(
                    key=key,
                    value={
                        "DATE_TIME": str(dt),
                        "TIMESTAMP": tstamp,
                        "TYPE": dtype,
                        "CONF_DATA": val["CONF_DATA"]
                    }
                )
            else:
                dt, tstamp, dtype = __calcDTime(data[key]["DATE_TIME"])
                QUEUE.update(
                    key=key,
                    value={
                        "DATE_TIME": str(dt),
                        "TIMESTAMP": tstamp,
                        "TYPE": dtype,
                        "SHELL": data[key]["EXECUTE"]["SHELL"],
                    }
                )
            yield key
    yield None


def handle_signal(
    signum: int,
    frame: signal
) -> None:
    """
    Function for processing system signals.
    ---------------------------------------
    :type signum: int
    :param signum: system signal number.

    :type frame: <class 'frame'>
    :param frame: current stack frame.
    """
    raise SystemExit(
        f"Signal {signum} received, shutting down gracefully..."
    )


def runningShellTask(
    sleep: int = 1,
    console: bool = False,
    ping_message: int = 10
) -> None:
    """
    Function to initialize the application.
    ---------------------------------------
    :type sleep: int
    :param sleep: sleep cycle for a while.

    :type console: bool
    :param console: output data to the console.

    :type ping_message: int
    :param ping_message: message time (sec).
    """
    try:
        cfg = initCfg()
        logger = getLogger(
            pathfile=cfg.LOGROTATION["LOGFILE"],
            console=console
        )
        logger.info(
            f"Getting settings: {cfg.CONFPATH}"
        )
        CopyConfDump(
            enable=cfg.CONFDUMP["ENABLE"],
            fromFilename=cfg.CONFPATH,
            toDirFilename=cfg.CONFDUMP["DIR"]
        )
        addShellTask(cfg.TASK)
        if cfg.LOGROTATION["ARCH"]["ENABLE"]:
            dt, tstamp, dtype = __calcDTime(
                cfg.LOGROTATION["ARCH"]["DATE_TIME"]
            )
            QUEUE.add(
                key="LOGROTATION",
                value={
                    "DATE_TIME": str(dt),
                    "TIMESTAMP": tstamp,
                    "TYPE": dtype,
                    "CONF_DATA": cfg.LOGROTATION
                }
            )
        logger.info(
            "Adding task queue: "
            f"size: {QUEUE.size()}\n"
            f"{QUEUE.get()}"
        )
        signal.signal(signal.SIGTERM, handle_signal)
        signal.signal(signal.SIGINT, handle_signal)
        pingMsg = time.time() + ping_message
        while True:
            worktime = time.time()
            cursor = updateShellTask(worktime, cfg.TASK)
            keyTask = next(cursor)
            if keyTask is not None:
                if keyTask == "LOGROTATION":
                    data: dict = QUEUE.get(key=keyTask)["CONF_DATA"]
                    logShellRotationTask(logger, data)
                else:
                    shellCmd: list = QUEUE.get(key=keyTask)["SHELL"]
                    {
                        logger.info(
                            f"shell:\n{os.popen(_).read().strip()}"
                        ) for _ in shellCmd
                    }
                    updateTask = {
                        keyTask: QUEUE.get(key=keyTask)
                    }
                    logger.info(
                        "Updated task queue: "
                        f"size: {QUEUE.size()}\n"
                        f"{updateTask}"
                    )
            if worktime >= pingMsg:
                logger.info("Server is active...")
                pingMsg = worktime + ping_message
            time.sleep(sleep)
    except KeyError as err:
        raise KeyError(
            "The configuration file (conf.json) was not accepted. "
            f"There is an error in the {err} field. "
            "Restore from a copy or edit the field yourself."
        )
