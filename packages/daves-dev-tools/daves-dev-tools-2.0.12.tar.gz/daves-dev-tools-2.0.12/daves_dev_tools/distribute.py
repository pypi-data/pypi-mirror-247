import functools
import os
import re
import sys
from distutils.core import run_setup
from subprocess import check_output
from time import time
from typing import Any, Callable, FrozenSet, Iterable, List

from .utilities import run_module_as_main, sys_argv_pop

lru_cache: Callable[..., Any] = functools.lru_cache


def _list_dist(
    directory: str, modified_at_or_after: float = 0.0
) -> FrozenSet[str]:
    dist_root: str = os.path.join(directory, "dist")
    dist_file: str
    dist_sub_directories: List[str]
    dist_files: Iterable[str]
    try:
        dist_root, dist_sub_directories, dist_files = next(
            iter(os.walk(dist_root))
        )
    except StopIteration:
        raise FileNotFoundError(
            f"No distributions could be found in {dist_root}"
        )
    dist_files = (
        os.path.join(dist_root, dist_file) for dist_file in dist_files
    )
    if modified_at_or_after:
        dist_files = filter(
            lambda dist_file: (  # noqa
                os.path.getmtime(dist_file) >= modified_at_or_after
            ),
            dist_files,
        )
    try:
        return frozenset(dist_files)
    except (NotADirectoryError, FileNotFoundError):
        return frozenset()


def _setup(directory: str) -> FrozenSet[str]:
    start_time: float = time()
    current_directory: str = os.path.abspath(os.path.curdir)
    os.chdir(directory)
    try:
        abs_setup: str = os.path.join(directory, "setup.py")
        setup_args: List[str] = ["sdist", "bdist_wheel"]
        print(f'{sys.executable} {abs_setup} {" ".join(setup_args)}')
        run_setup(abs_setup, setup_args)
    finally:
        os.chdir(current_directory)
    return _list_dist(directory, modified_at_or_after=start_time)


def _get_help() -> bool:
    """
    If `-h` or `--help` keyword arguments are provided,
    retrieve the repository credentials and store them in the "TWINE_USERNAME"
    and "TWINE_PASSWORD" environment variables.
    """
    if set(sys.argv) & {"-h", "--help", "-H", "--HELP"}:
        help_: str = check_output(
            (sys.executable, "-m", "twine", "upload", "-h"),
            encoding="utf-8",
            universal_newlines=True,
        ).strip()
        help_ = re.sub(
            r"\btwine upload\b",
            "daves-dev-tools distribute",
            help_,
        )
        help_ = re.sub(
            (
                r"(\n\s*)dist \[dist \.\.\.\](?:.|\n)+"
                r"(\npositional arguments:\s*\n\s*)(?:.|\n)+"
                r"(\noptional arguments:\s*\n)"
            ),
            (
                r"\1[directory]"
                r"\n\2directory             "
                "The root directory path for the project."
                r"\n\3"
            ),
            help_,
        )
        print(help_)
        return True
    return False


def _dist(
    directory: str, distributions: FrozenSet[str], echo: bool = True
) -> None:
    run_module_as_main(
        "twine",
        arguments=(["upload"] + sys.argv[1:] + list(sorted(distributions))),
        directory=directory,
        echo=False,
    )


def _cleanup(directory: str) -> None:
    current_directory: str = os.path.abspath(os.path.curdir)
    os.chdir(directory)
    try:
        run_setup(os.path.join(directory, "setup.py"), ["clean", "--all"])
    finally:
        os.chdir(current_directory)


def main() -> None:
    if not _get_help():
        directory: str = sys_argv_pop(depth=2, default=".")  # type: ignore
        directory = os.path.abspath(directory).rstrip("/")
        try:
            _dist(directory, _setup(directory))
        finally:
            _cleanup(directory)


if __name__ == "__main__":
    main()
