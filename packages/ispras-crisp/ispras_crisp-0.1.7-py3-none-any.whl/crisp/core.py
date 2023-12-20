import os
import subprocess
from enum import Enum
from typing import List, Optional

import git
import pycodestyle
from colorama import Fore, Style
from wcmatch import glob

from crisp import CrispError
from crisp.config import CrispConfig, FileSelectionMode, ReturnCode, process_config
from crisp.report import CustomPycodestyleReport, print_report

EMPTY_TREE_SHA = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


def run_crisp(
    action: str,
    mode: FileSelectionMode,
    workdir: str = ".",
    include: Optional[List[str]] = None,
    force_exclude: bool = False,
    no_pyproject_update: bool = False,
) -> ReturnCode:
    """Запуск Crisp в режиме ``action``.

    :param action: режим (``lint`` для проверки или ``fix`` для исправления файлов)
    :param mode: стратегия выбора файлов
    :param workdir: директория проверяемого Git-репозитория либо одна из ее
        поддиректорий
    :param include: список полных ненормированных путей, дополнительный к mode фильтр
    :param force_exclude: исключать файл согласно exclude, даже если он передан как
        позиционный аргумент
    :param no_pyproject_update: запретить ли обновление pyproject.toml (при
        параллельном запуске нескольких экземпляров Crisp требуется значение True)
    :returns: 0 при отсутствии ошибок линтинга, 1 иначе
    :raises CrispError: в случае отсутствия валидных Git-репозитория и конфигурации

    :group: functions
    """
    git_repo = get_git_repo(workdir)

    if include is not None:
        for idx, include_item in enumerate(include):
            include[idx] = os.path.join(os.getcwd(), include_item.lstrip(os.path.sep))

    os.chdir(git_repo.working_tree_dir)  # pyre-ignore
    config = process_config(
        git_repo.working_tree_dir, no_pyproject_update
    )  # pyre-ignore

    files = list_files(git_repo, mode, config, include, force_exclude)
    if not files:
        print(f"{Fore.LIGHTYELLOW_EX}No files to check.")
        return ReturnCode.no_error

    if action == "fix":
        return fix(files)

    pycodestyle_guide = pycodestyle.StyleGuide(
        max_line_length=config.line_length,
        ignore=config.ignore_errors_pycodestyle,
        reporter=CustomPycodestyleReport,
    )
    pycodestyle_report = pycodestyle_guide.check_files(files)

    ruff_proc = subprocess.run(
        ["ruff", "check", "--output-format", "json", *files],
        capture_output=True,
        text=True,
    )
    black_proc = subprocess.run(
        ["black", "--check", *files], capture_output=True, text=True
    )
    ruff_output = None if ruff_proc.returncode == 0 else ruff_proc.stdout
    black_output = None if black_proc.returncode == 0 else black_proc.stderr

    rc = print_report(config.workdir, pycodestyle_report, ruff_output, black_output)
    rc |= check_unable_to_process(ruff_proc.stderr)

    return rc


def fix(files: List[str]) -> ReturnCode:
    """Исправить файлы ``files``.

    :param files: список относительных путей к файлам, которые потенциально будут
        исправлены
    :returns: 1, если не удалось проанализировать некоторые файлы, 0 иначе

    :group: functions
    """
    modified_times = {path: os.stat(path).st_mtime for path in files}

    ruff_proc = subprocess.run(
        ["ruff", "check", "--fix-only", *files], capture_output=True, text=True
    )
    _black_proc = subprocess.run(["black", *files], capture_output=True, text=True)

    fixed_files = sorted(
        p for p, t in modified_times.items() if os.stat(p).st_mtime > t
    )
    if not fixed_files:
        print(f"{Fore.LIGHTYELLOW_EX}Nothing to fix.")
    for path in fixed_files:
        print(f"Fixed {Fore.LIGHTBLUE_EX}{path}")

    return check_unable_to_process(ruff_proc.stderr)


def check_unable_to_process(ruff_stderr: str) -> ReturnCode:
    if len(ruff_stderr) > 0:
        print(f"{Fore.RED}Ruff was unable to process some files:")
        for line in ruff_stderr.strip().split("\n"):
            print(f"    {line}")
        return ReturnCode.lint_error

    return ReturnCode.no_error


def get_git_repo(workdir: str) -> git.Repo:
    try:
        repo = git.Repo(workdir, search_parent_directories=True)
    except git.InvalidGitRepositoryError as err:
        raise CrispError(
            f"Could not find a Git repo in "
            f"{Fore.LIGHTYELLOW_EX}{workdir}{Style.RESET_ALL} or its parents.\n"
            f"Crisp only works in Git repos with {Fore.LIGHTYELLOW_EX}pyproject.toml"
            f"{Style.RESET_ALL} file."
        ) from err

    if repo.bare:
        raise CrispError("Bare Git repos are not supported.")

    return repo


class ExcludePatternKind(Enum):
    exclude = 1
    include = 2


class ExcludePattern:
    """Шаблон для исключения либо включения файлов в список обрабатываемых Crisp.

    :group: classes
    """

    def __init__(
        self, raw_pattern: str, kind: ExcludePatternKind, workdir: str
    ) -> None:
        self.kind = kind

        is_directory = raw_pattern.endswith(os.path.sep)
        no_trailing_slash = raw_pattern.rstrip(os.path.sep)

        is_path = os.path.sep in no_trailing_slash or no_trailing_slash in [
            "**",
            ".",
            "..",
        ]

        if kind == ExcludePatternKind.include:
            relpath = os.path.relpath(raw_pattern, start=workdir)
        else:
            if is_path:
                relpath = raw_pattern.lstrip(os.path.sep)
            else:
                relpath = os.path.join("**", raw_pattern)
            relpath = os.path.normpath(relpath)

        if relpath == ".":
            relpath = "**"

        if relpath.endswith("**"):
            self.pattern = relpath
        else:
            with_globstar = os.path.join(relpath, "**")
            if is_directory:
                self.pattern = with_globstar
            else:
                self.pattern = [with_globstar, relpath]

    def match(self, actual_file: str) -> bool:
        return glob.globmatch(actual_file, self.pattern, flags=glob.GLOBSTAR)

    def oldest_matching_parent(self, actual_file: str) -> str:
        matching_parent = actual_file

        while True:
            parent_dir = os.path.dirname(matching_parent)
            if not self.match(parent_dir + os.path.sep):
                break

            matching_parent = parent_dir
            if matching_parent == "":
                break

        return matching_parent


def list_files(
    git_repo: git.Repo,
    mode: FileSelectionMode,
    config: CrispConfig,
    include: Optional[List[str]] = None,
    force_exclude: bool = False,
) -> List[str]:
    """Получить список *существующих* файлов для обработки.

    Функция должна запускаться только с корневой директорией Git-репозитория в качестве
    текущей рабочей директории ``os.getcwd()``.

    :param git_repo: Git-репозиторий
    :param mode: стратегия выбора файлов
    :param config: конфигурация Crisp
    :param include: список полных ненормированных путей, дополнительный к mode фильтр
    :param force_exclude: исключать файл согласно exclude, даже если он передан как
        позиционный аргумент
    :raises CrispError: в случае невалидности Git-репозитория (например, отсутствия
        коммитов)

    :group: functions
    """

    def _from_working_tree(include_staged):
        if include_staged:
            against = "HEAD" if git_repo.head.is_valid() else EMPTY_TREE_SHA
            return git_repo.git.diff(against, name_only=True)
        else:
            return git_repo.git.diff(None, name_only=True)

    def _from_commit_diff(branch):
        if not git_repo.head.is_valid():
            raise CrispError(
                "Repo "
                f"{Fore.LIGHTYELLOW_EX}{git_repo.working_tree_dir}{Style.RESET_ALL} "
                "has no commits."
            )
        if not git_repo.head.commit.parents:
            against = EMPTY_TREE_SHA
        elif branch is not None:
            against = branch
        else:
            against = "HEAD~1"

        return git_repo.git.diff(f"{against}..HEAD", name_only=True)

    if mode == FileSelectionMode.default:
        comma_sep = _from_working_tree(include_staged=True)
    elif mode == FileSelectionMode.modified:
        comma_sep = _from_working_tree(include_staged=False)
    elif mode == FileSelectionMode.latest_commit:
        comma_sep = _from_commit_diff(branch=None)
    elif mode == FileSelectionMode.diff_master:
        comma_sep = _from_commit_diff(branch=config.default_branch)
    else:
        comma_sep = git_repo.git.ls_files()

    files = comma_sep.split("\n")

    patterns = [
        ExcludePattern(pattern, ExcludePatternKind.exclude, workdir=os.getcwd())
        for pattern in config.exclude_files
    ]
    if include is not None:
        patterns += [
            ExcludePattern(full_path, ExcludePatternKind.include, workdir=os.getcwd())
            for full_path in include
        ]
    else:
        patterns += [
            ExcludePattern("**", ExcludePatternKind.include, workdir=os.getcwd())
        ]

    return exclude_files(
        [f for f in files if os.path.isfile(f)], patterns, force_exclude
    )


def exclude_files(
    files: List[str], patterns: List[ExcludePattern], force_exclude: bool = False
) -> List[str]:
    """Отфильтровать список файлов согласно шаблонам.

    :param files: список относительных путей внутри Git-репозитория
    :param patterns: список glob-шаблонов для исключения/включения файлов
    :param force_exclude: исключать файл согласно exclude, даже если он передан как
        позиционный аргумент
    :returns: отфильтрованный список относительных путей

    :group: functions
    """
    filtered_files: List[str] = []

    for file_ in files:
        if os.path.splitext(file_)[1] != ".py":
            continue

        exclude_matches: List[ExcludePattern] = []
        include_matches: List[ExcludePattern] = []

        for pattern in patterns:
            if pattern.match(file_):
                append_to = (
                    exclude_matches
                    if pattern.kind == ExcludePatternKind.exclude
                    else include_matches
                )
                append_to.append(pattern)

        if not include_matches or (exclude_matches and force_exclude):
            continue
        elif not exclude_matches:
            filtered_files.append(file_)
            continue

        most_specific_exclude = max(
            pattern.oldest_matching_parent(file_) for pattern in exclude_matches
        )
        most_specific_include = max(
            pattern.oldest_matching_parent(file_) for pattern in include_matches
        )

        if most_specific_include >= most_specific_exclude:
            filtered_files.append(file_)

    return filtered_files
