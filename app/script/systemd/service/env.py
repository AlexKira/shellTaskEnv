import os
import sys

BASEDIR = os.getenv("SHELL_WORKDIR", "/opt/shellTaskEnv")
sys.path.append(f"{BASEDIR}/app")


def fromBaseExportSchema() -> object:
    """
    Function for importing modules from the application.
    ----------------------------------------------------
    :rtype: object
    :returns: <class 'core.schema.BaseExportSchema'>.
    """
    from exec.runTask import initCfg
    return initCfg()


def addEnvFile() -> None:
    """
    File creation function for virtual environment.
    """
    obj = fromBaseExportSchema()
    with open(f"{BASEDIR}/app/script/systemd/service/.env", "w") as file:
        export = (
            "#!/bin/bash\n"
            "export SHELL_LOGROTATION="
            f"{os.path.dirname(obj.LOGROTATION['LOGFILE']['FILENAME'])}\n"
            "export SHELL_LOGROTATION_ARCH="
            f"{os.path.dirname(obj.LOGROTATION['ARCH']['DIR'])}\n"
            f"export SHELL_CONFPATH={os.path.dirname(obj.CONFPATH)}\n"
            f"export SHELL_CONFDUMP={os.path.dirname(obj.CONFDUMP['DIR'])}\n"
        )
        file.write(export)


if __name__ == "__main__":
    addEnvFile()
