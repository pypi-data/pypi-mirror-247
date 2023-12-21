from ._execute import execute_python as execute_python
from .pyinstaller import PackageInstaller as PackageInstaller, PyInstaller as PyInstaller
from enum import IntEnum
from typing import Any, Final

class SmartAutoModuleCombineMode(IntEnum):
    DISABLE: Final[int]
    FOLDER_ONLY: Final[int]
    ALL_INTO_ONE: Final[int]

class Builder:
    __PATH: Final[str]
    __CACHE_FOLDERS_NEED_REMOVE: Final[tuple[str, ...]]
    __DIST_DIR: Final[str]
    @classmethod
    def __remove_cache(cls, path: str) -> None: ...
    @staticmethod
    def remove(*path: str) -> None: ...
    @staticmethod
    def copy(files: tuple[str, ...], target_folder: str) -> None: ...
    @classmethod
    def __clean_up(cls) -> None: ...
    @classmethod
    def __combine(cls, _dir_path: str) -> None: ...
    @classmethod
    def compile(cls, source_folder: str, target_folder: str = ..., additional_files: tuple[str, ...] = ..., ignore_key_words: tuple[str, ...] = ..., smart_auto_module_combine: SmartAutoModuleCombineMode = ..., remove_building_cache: bool = ..., update_the_one_in_sitepackages: bool = ..., include_pyinstaller_program: bool = ..., options: dict[str, Any] = ...) -> None: ...
    @classmethod
    def build(cls) -> None: ...
    @classmethod
    def upload(cls, confirm: bool = ...) -> None: ...
