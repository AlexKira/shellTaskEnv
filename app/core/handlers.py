import os
import time
import shutil
import tarfile
import zipfile
from datetime import datetime
from typing import (
    List,
    Dict
)


class LogArch(object):
    """Class for archiving log files."""

    @classmethod
    def targz(
        cls,
        archName: str,
        fromDir: str,
        toDir: str,
        typeArch: str,
        formatDt: str
    ) -> Dict[str, str]:
        out = dict()
        packed = list()
        """Method targz archiving."""
        try:
            frmtDt = datetime.now().strftime(formatDt)
            save_arch_name = (
                f"{toDir}/{archName}_{frmtDt}.tar.{typeArch}"
            )
            with tarfile.open(
                save_arch_name, "w:gz"
            ) as tarGz:
                for file in os.listdir(fromDir):
                    pathFile = f"{fromDir}/{file}"
                    if pathFile != toDir:
                        tarGz.add(
                            pathFile,
                            arcname=os.path.relpath(
                                pathFile, fromDir
                            )
                        )
                        packed.append(pathFile)

            out.update(
                {
                    "packed": packed,
                    "arch_name": save_arch_name
                }
            )
            return out
        except Exception as err:
            raise err

    @classmethod
    def zipp(
        cls,
        archName: str,
        fromDir: str,
        toDir: str,
        typeArch: str,
        formatDt: str
    ) -> None:
        """Method zip archiving."""
        out = dict()
        packed = list()
        try:
            frmtDt = datetime.now().strftime(formatDt)
            save_arch_name = (
                f"{toDir}/{archName}_{frmtDt}.{typeArch}"
            )
            with zipfile.ZipFile(
                save_arch_name, "w",
                zipfile.ZIP_DEFLATED
            ) as zipf:
                for file in os.listdir(fromDir):
                    pathFile = f"{fromDir}/{file}"
                    if pathFile != toDir:
                        zipf.write(
                            pathFile,
                            arcname=os.path.relpath(
                                pathFile, fromDir
                            )
                        )
                        packed.append(pathFile)

            out.update(
                {
                    "packed": packed,
                    "arch_name": save_arch_name
                }
            )
            return out
        except Exception as err:
            raise err

    def __init__(
        self,
        fromDir: str,
        toDir: str,
        archName: str,
        typeArch: str,
        formatDt: str = "%Y-%m-%d_%H:%M:%S"
    ) -> None:
        """
        LogArch constructor that archives log files.
        --------------------------------------------
        :type fromDir: str
        :param fromDir: path to the archiving directory.

        :type toDir: str
        :param toDir: path to the directory in which the \
            archive will be created.

        :type archName: str
        :param archName: Archived directory name

        :type typeArch: str
        :param typeArch: Archive type "zip" or "gz", default name "gz"

        :type formatDt: str
        :param formatDt: The default date and time format \
            for the archive directory is '%Y-%m-%d_%H:%M:%S'.
        """
        self.out: list[str] = None
        if not os.path.isdir(toDir):
            os.makedirs(toDir)
        if typeArch == "gz":
            self.out = self.targz(
                archName=archName,
                fromDir=fromDir,
                toDir=toDir,
                typeArch=typeArch,
                formatDt=formatDt
            )
        elif typeArch == "zip":
            self.out = self.zipp(
                archName=archName,
                fromDir=fromDir,
                toDir=toDir,
                typeArch=typeArch,
                formatDt=formatDt
            )
        else:
            raise TypeError(
                "Invalid directory archiving type. Can be 'gz' or 'zip'."
            )


class TruncateLogFile(object):
    """Class for truncating the log file."""

    @classmethod
    def truncate(
        cls,
        abspath_filename: str
    ) -> Dict[str, str]:
        """Method truncate file."""
        try:
            if not os.path.isfile(abspath_filename):
                raise FileNotFoundError(
                    f"Error. File '{abspath_filename}' not found"
                )
            status = os.system(
                f"truncate -s 0 {abspath_filename}"
            )
            if status != 0:
                raise SystemError(
                    "File cleanup completed with an error."
                    "Check file availability."
                )
            else:
                return {
                    "truncate": "ok",
                    "filename": abspath_filename
                }
        except Exception as err:
            raise err

    def __init__(
        self,
        truncate: bool,
        abspath_filename: str
    ) -> None:
        """
        TruncateLogFile constructor to truncate the log file.
        -----------------------------------------------------
        :type truncate: bool
        :param truncate: on (True) and off (False).

        :type abspath_filename: str
        :param abspath_filename: name of the file to be truncate.
        """
        self.out: dict[str, str] = None
        if truncate:
            self.out = self.truncate(abspath_filename)


class DeleteLogArch(object):
    """
    Сlass for deleting archive files and directories.
    """

    @classmethod
    def delete(
        cls,
        days: int,
        dirpath: str
    ) -> List[str]:
        """
        Method for deleting directories and files.
        """
        out = list()
        curTime = time.time() - (days * 86400)
        for filename in os.listdir(dirpath):
            pathfile = os.path.join(dirpath, filename)
            if os.path.isfile(pathfile):
                file_mod_time = os.path.getmtime(pathfile)
                if file_mod_time < curTime:
                    os.remove(pathfile)
                    out.append(pathfile)
        return out

    def __init__(
        self,
        enable: bool,
        dirpath: str,
        days: int
    ) -> None:
        """
        DeleteLogArch constructor for deleting archive files and directories.
        ---------------------------------------------------------------------
        :type enable: bool
        :param enable: on (True) and off (False).

        :type dirpath: str
        :param dirpath: path to the directory where the file is located.

        :type days: int
        :param days: number of days until deletion.
        """
        self.out: List[str] = None
        if enable:
            try:
                self.out = self.delete(
                    dirpath=dirpath,
                    days=days
                )
            except NotADirectoryError as err:
                raise NotADirectoryError(
                    f"Error: Please specify the file directory. {err}"
                )


class CopyConfDump(object):
    """Class for copying files."""

    @classmethod
    def copy(
        cls,
        enable: bool,
        fromFilename: str,
        toDirFilename: str,
    ) -> None:
        """Method copy."""
        if enable:
            toDir = os.path.dirname(toDirFilename)
            if not os.path.isfile(fromFilename):
                raise FileNotFoundError(
                    "Error. File not found."
                )
            if not os.path.isdir(toDir):
                os.makedirs(toDir)
            shutil.copy(fromFilename, toDirFilename)

    def __init__(
        self,
        enable: bool,
        fromFilename: str,
        toDirFilename: str,
    ) -> None:
        """
        CopyConfDump constructor for copying files.
        -------------------------------------------
        :type enable: bool
        :param enable: on (True) and off (False).

        :type fromFilename: str
        :param fromFilename: name of the file to copy.

        :type toDirFilename: str
        :param toDirFilename: directory name where to copy.
        """
        try:
            self.copy(enable, fromFilename, toDirFilename)
        except shutil.ExecError as err:
            raise err
