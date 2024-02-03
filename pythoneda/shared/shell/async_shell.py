# vim: set fileencoding=utf-8
"""
pythoneda/shared/shell/async_shell.py

This file defines the AsyncShell class.

Copyright (C) 2024-today rydnr's pythoneda-shared-pythonlang/shell

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import asyncio
import os
from pythoneda import attribute, BaseObject
import shlex
import subprocess
import tempfile
from typing import List


class AsyncShell(BaseObject):

    """
    Represents an asynchronous shell.

    Class name: AsyncShell

    Responsibilities:
        - Execute shell commands in an asynchronous interface.

    Collaborators:
        - asyncio
    """

    def __init__(self, args: List, folder: str = None):
        """
        Creates an AsyncShell instance.
        :param args: The args to execute.
        :type args: List[str]
        :param folder: The folder to run the args.
        :type folder: str
        """
        super().__init__()
        self._args = args
        self._folder = folder

    @property
    @attribute
    def args(self) -> List[str]:
        """
        Retrieves the argument list.
        :return: Such list.
        :rtype: List[str]
        """
        return self._args

    @property
    @attribute
    def folder(self) -> str:
        """
        Retrieves the folder.
        :return: Such folder.
        :rtype: str
        """
        return self._folder

    async def run_in_a_temporary_folder(self):
        """
        Runs the arguments in a temporary folder.
        :return: The process instance (with return code, stdout and stderr)
        :rtype: process
        """
        with tempfile.TemporaryDirectory() as tmp_folder:
            result = await self._run_in(tmp_folder)

        return result

    async def _run_in(self, folder: str):
        """
        Runs the arguments in given folder.
        :param folder: The folder to run the args in.
        :type folder: str
        :return: The process instance (with return code, stdout and stderr)
        :rtype: process
        """
        escaped_args = [shlex.quote(arg) for arg in self.args]
        result = await asyncio.create_subprocess_shell(
            " ".join(escaped_args),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=folder,
            bufsize=0,
            universal_newlines=False,
            env={"PATH": os.environ["PATH"]},
        )

        await result.communicate()

        return result

    async def run(self):
        """
        Runs the shell.
        :return: The process instance (with return code, stdout and stderr)
        :rtype: process
        """
        if self.folder:
            result = await self._run_in(self.folder)
        else:
            result = await self._run_in_temporary_folder()
        return result


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
