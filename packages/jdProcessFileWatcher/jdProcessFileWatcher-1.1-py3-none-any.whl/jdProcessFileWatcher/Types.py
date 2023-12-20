from .FileAction import FileAction
import dataclasses
import datetime

@dataclasses.dataclass
class FileChangedData:
    action: FileAction
    path: str
    time: datetime.time
    pid: int
    process_name: str


@dataclasses.dataclass
class StartProcessInfo:
    cmdline: list[str]
    working_directory: str | None = None
