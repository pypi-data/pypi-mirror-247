from PyQt6.QtCore import QObject, QProcess, QCoreApplication, pyqtSignal
from .Types import FileChangedData, StartProcessInfo
from .Constants import USE_STRACE_SETTINGS_VALUE
from .FileAction import FileAction
from .Functions import is_flatpak
from typing import TYPE_CHECKING
import configparser
import subprocess
import datetime
import sys
import os
import re


if TYPE_CHECKING:
    from .Environment import Environment


_FILE_FUNCTIONS_REG_EX = re.compile(r'\d+<[A-z|0-9| ]+> \d{2}:\d{2}:\d{2} \w+\(\w+<[\/|A-z|0-9|.]+>(, "[\/|A-z|0-9|.]+",)?')
_PATH_REG_EX = re.compile(r"(?<=<)[\/|A-z|0-9.]+(?=>)")
_PATH2_REG_EX = re.compile(r'(?<=>, ")[\/|A-z|0-9|.]+(?=",)')
_ACTION_REG_EX = re.compile(r"(?<=\d{2}:\d{2}:\d{2} )\w+?(?=\()")
_PROCESS_PART_REG_EX = re.compile(r"\d+<[A-z|0-9| ]+>(?= )")
_PROCESS_NAME_REG_EX = re.compile(r"(?<=\d<)[A-z|0-9| ]+(?=>)")
_PID_REG_EX = re.compile(r"\d+(?=<)")


class StraceWrapper(QObject):
    file_changed = pyqtSignal(FileChangedData)
    process_started = pyqtSignal(int)
    process_finished = pyqtSignal()

    def __init__(self, env: "Environment") -> None:
        super().__init__()

        self._env = env
        self._process = QProcess(self)

        self._process.readyReadStandardError.connect(self._data_read)
        self._process.started.connect(lambda: self.process_started.emit(self._process.processId()))
        self._process.finished.connect(lambda: self.process_finished.emit())

        self._proc_info_cache: dict[int, tuple[str, str]] = {}

    def _process_file_handle(self, line: str) -> None:
        action_match = _ACTION_REG_EX.search(line)
        action_string = action_match.group()

        if f"{action_string}(AT_FDCWD<" in line and line.endswith('",'):
            path = _PATH2_REG_EX.search(line).group()
        else:
            path = _PATH_REG_EX.search(line[action_match.start():]).group()

        process_part = _PROCESS_PART_REG_EX.search(line).group()
        pid = int(_PID_REG_EX.search(process_part).group())
        process_name = _PROCESS_NAME_REG_EX.search(process_part).group()

        match action_string:
            case "openat":
                action = FileAction.OPEN
            case "close":
                action = FileAction.CLOSE
            case "read" | "pread64":
                action = FileAction.READ_FILE
            case "write" | "pwrite64":
                action = FileAction.WRITE_FILE
            case "statx" | "newfstatat":
                action = FileAction.READ_STATUS
            case "getdents64":
                action = FileAction.READ_DIRECTORY
            case "fchmod":
                action = FileAction.CHANGE_PERMISSION
            case "statfs" | "fstatfs":
                action = FileAction.READ_FILESYSTEM_INFO
            case "fchdir":
                action = FileAction.CHANGE_WORKING_DIRECTORY
            case "readlinkat":
                action = FileAction.READ_LINK
            case "faccessat2":
                action = FileAction.READ_PERMISSION
            case "lseek" | "ioctl" | "fcntl" | "fallocate":
                return
            case _:
                action = FileAction.UNKNOWN
                print(QCoreApplication.translate("StraceWrapper", "Unknown syscall: {{syscall}}").replace("{{syscall}}", action_string), file=sys.stderr)

        data = FileChangedData(action, path, datetime.datetime.now(), pid, process_name)

        self.file_changed.emit(data)

    def _parse_line(self, line: str) -> None:
        match = _FILE_FUNCTIONS_REG_EX.search(line)
        if match is not None:
            self._process_file_handle(match.group())

    def _data_read(self) -> None:
        output = bytes(self._process.readAllStandardError()).decode("utf-8")

        for line in output.splitlines():
            self._parse_line(line)

    def _flatpak_to_host_path(self, path: str, app_path: str, runtime_path: str) -> str:
        if path.startswith("/app"):
            return os.path.join(app_path, path.removeprefix("/app/"))
        elif path.startswith("/usr"):
            return os.path.join(runtime_path, path.removeprefix("/usr/"))
        else:
            return path

    def _get_ld_path(self, app_path: str, runtime_path: str) -> str:
        result = subprocess.run(["ldconfig", "-p"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if line.strip().startswith("ld-linux"):
                return self._flatpak_to_host_path(line.split(" => ")[1].strip(), app_path, runtime_path)

    def _get_all_lib_paths(self, app_path: str, runtime_path: str) -> list[str]:
        path_list: list[str] = []
        result = subprocess.run(["ldconfig", "-v"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if not line.startswith("\t"):
                path_list.append(self._flatpak_to_host_path(line.split(":")[0], app_path, runtime_path))
        return path_list

    def _get_strace_command(self, root: bool) -> list[str]:
        if self._env.settings.get("useStrace") == USE_STRACE_SETTINGS_VALUE.BUILT_IN and is_flatpak():
            config = configparser.ConfigParser()
            config.read("/.flatpak-info")
            app_path = config["Instance"]["app-path"]
            runtime_path = config["Instance"]["runtime-path"]
            lib_paths = self._get_all_lib_paths(app_path, runtime_path)
            ld_path = self._get_ld_path(app_path, runtime_path)
            strace_path = os.path.join(app_path, "bin", "strace")

            if root:
                command = ["flatpak-spawn", "--host", "pkexec", "--disable-internal-agent", ld_path, "--library-path", ":".join(lib_paths), strace_path]
            else:
                command = ["flatpak-spawn", "--host", ld_path, "--library-path", ":".join(lib_paths), strace_path]
        elif  self._env.settings.get("useStrace") == USE_STRACE_SETTINGS_VALUE.BUILT_IN and self._env.settings.get("customStracePath") != "":
            if is_flatpak():
                if root:
                    command = ["flatpak-spawn", "--host", "pkexec", "--disable-internal-agent", self._env.settings.get("customStracePath")]
                else:
                    command = ["flatpak-spawn", "--host", self._env.settings.get("customStracePath")]
            else:
                if root:
                    command = ["pkexec", "--disable-internal-agent", self._env.settings.get("customStracePath")]
                else:
                    command = [self._env.settings.get("customStracePath")]
        else:
            if is_flatpak():
                if root:
                    command = ["flatpak-spawn", "--host", "pkexec", "--disable-internal-agent", "strace"]
                else:
                    command = ["flatpak-spawn", "--host", "strace"]
            else:
                if root:
                    command = ["pkexec", "--disable-internal-agent", "strace"]
                else:
                    command = ["strace"]

        return command + self.get_strace_arguments()

    def get_strace_arguments(self) -> list[str]:
        return ["-fyyt", "-e", "trace=%file,%desc", "--decode-pids=comm", "--output", "/dev/stderr"]

    def start_process(self, info: StartProcessInfo) -> None:
        command = self._get_strace_command(False) + info.cmdline

        self._process.kill()

        if info.working_directory is not None:
            self._process.setWorkingDirectory(info.working_directory)

        self._process.start(command[0], command[1:])

    def attach_process(self, pid: int) -> None:
        command = self._get_strace_command(True) + ["-p", str(pid)]

        self._process.kill()

        self._process.start(command[0], command[1:])

    def load_log_file(self, path: str) -> None:
        self._process.kill()

        with open(path, "r", encoding="utf-8") as f:
            while True:
                line = f.readline()

                if not line:
                    break

                self._parse_line(line)

    def _get_strace_child_pid(self) -> int:
        if is_flatpak():
            return int(subprocess.run(["flatpak-spawn", "--host", "pgrep", "-P", str(self._process.processId())], capture_output=True, text=True, check=True).stdout.strip())
        else:
            return int(subprocess.run(["pgrep", "-P", str(self._process.processId())], capture_output=True, text=True, check=True).stdout.strip())

    def _send_process_signal(self, signal: str) -> None:
        if is_flatpak():
            subprocess.run(["flatpak-spawn", "--host", "kill", signal, str(self._get_strace_child_pid())], check=True)
        else:
            subprocess.run(["kill", signal, str(self._get_strace_child_pid())], check=True)

    def terminate_process(self) -> None:
        self._process.terminate("-SIGTERM")

    def kill_process(self) -> None:
        self._send_process_signal("-SIGKILL")
