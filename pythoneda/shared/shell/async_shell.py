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
from pathlib import Path
from pythoneda.shared import attribute, BaseObject
import shlex
import subprocess
import tempfile
from typing import Dict, List, Tuple


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

    async def run_in_a_temporary_folder(
        self, communicate: bool = True, env: Dict = None, charset: str = "utf-8", **kwds
    ) -> Tuple[asyncio.subprocess.Process, str, str]:
        """
        Runs the arguments in a temporary folder.
        :param communicate: Whether to communicate with the process or not.
        :type communicate: bool
        :param env: The environment to use.
        :rtype env: Dict
        :param charset: The charset to decode the stdout and stderr (if 'communicate' is True).
        :rtype charset: str
        :param kwds: Additional keywords.
        :type kwds: Dict
        :return: The tuple (asyncio.subprocess.Process, stdout, stderr).
        :rtype: Tuple[asyncio.subprocess.Process, str, str]
        """
        with tempfile.TemporaryDirectory() as tmp_folder:
            result = await self._run_in(
                self.args, tmp_folder, communicate, env, charset, **kwds
            )

        return result

    async def run(
        self, communicate: bool = True, env: Dict = None, charset: str = "utf-8", **kwds
    ) -> Tuple[asyncio.subprocess.Process, str, str]:
        """
        Runs the shell.
        :param communicate: Whether to communicate with the process or not.
        :type communicate: bool
        :param env: The environment to use.
        :rtype env: Dict
        :param charset: The charset to decode the stdout and stderr (if 'communicate' is True).
        :rtype charset: str
        :param kwds: Additional keywords.
        :type kwds: Dict
        :return: The tuple (asyncio.subprocess.Process, stdout, stderr).
        :rtype: Tuple[asyncio.subprocess.Process, str, str]
        """
        if self.folder:
            result = await self._run_in(
                self.args, self.folder, communicate, env, charset, **kwds
            )
        else:
            result = await self.run_in_a_temporary_folder(
                communicate, env, charset, **kwds
            )

        return result

    async def _run_in(
        self,
        args: List[str],
        folder: str,
        communicate: bool = True,
        env: Dict = None,
        charset: str = "utf-8",
        **kwds,
    ) -> Tuple[asyncio.subprocess.Process, str, str]:
        """
        Runs the arguments in given folder.
        :param args: The command-line arguments.
        :type args: List[str]
        :param folder: The folder to run the args in.
        :type folder: str
        :param communicate: Whether to communicate with the process or not.
        :type communicate: bool
        :param env: The environment to use.
        :type env: Dict
        :param charset: The charset to decode the stdout and stderr (if 'communicate' is True).
        :type charset: str
        :param kwds: Additional keywords.
        :type kwds: Dict
        :return: The tuple (asyncio.subprocess.Process, stdout, stderr).
        :rtype: Tuple[asyncio.subprocess.Process, str, str]
        """
        if env is None:
            env = {
                "PATH": os.environ.get("PATH", None),
                "TMPDIR": os.environ.get("TMPDIR", None),
            }

        cleanup_after = False
        temp_folder = env.get("TMPDIR", None)
        if temp_folder and not os.path.exists(temp_folder):
            cleanup_after = True
            Path(temp_folder).mkdir()

        merged_keywords = {
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "cwd": folder,
            "env": env,
        }

        merged_keywords.update(kwds)

        if merged_keywords.get("bufsize", None) is None:
            merged_keywords["bufsize"] = 0
        if merged_keywords.get("universal_newlines", None) is None:
            merged_keywords["universal_newlines"] = False

        escaped_args = [shlex.quote(str(arg)) for arg in args]
        process = await asyncio.create_subprocess_shell(
            " ".join(escaped_args), **merged_keywords
        )

        if communicate:
            stdout, stderr = await process.communicate()
            stdout = stdout.decode(charset)
            stderr = stderr.decode(charset)
        else:
            stdout = None
            stderr = None

        if cleanup_after:
            Path(temp_folder).rmdir()

        return (process, stdout, stderr)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
