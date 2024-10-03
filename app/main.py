# -*- coding: utf-8 -*-
from exec.runTask import (
    getLogger,
    runningShellTask
)


def main() -> None:
    """Main function to launch the application."""
    rootLogger = getLogger(
        name="shellTaskEnvRoot"
    )
    try:
        rootLogger.info("Server is running...")
        runningShellTask()
    except SystemExit as err:
        rootLogger.warning(err)
    except Exception as err:
        rootLogger.error(err)
        raise err
    finally:
        rootLogger.info("Server is stopping...")


if __name__ == "__main__":
    main()
