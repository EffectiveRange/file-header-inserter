# SPDX-FileCopyrightText: 2024 Ferenc Nandor Janky <ferenj@effective-range.com>
# SPDX-FileCopyrightText: 2024 Attila Gombos <attila.gombos@effective-range.com>
# SPDX-License-Identifier: MIT

import os
import re
from typing import Optional

from context_logger import get_logger

from header_adder import HeaderInserter, ILanguageDetector

log = get_logger('HeaderAdder')


class HeaderAdder(object):

    def __init__(self, language_detector: ILanguageDetector, header_inserter: HeaderInserter,
                 exclude_dirs: list[str], exclude_files: list[str]) -> None:
        self._language_detector = language_detector
        self._header_inserter = header_inserter
        self._exclude_dirs = exclude_dirs
        self._exclude_files = exclude_files

    def add_header_recursively(self, root_path: str, header_text: str) -> None:
        log.info('Processing directory', path=root_path)
        for path in os.listdir(root_path):
            path = os.path.join(root_path, path)
            if os.path.isdir(path):
                if self._is_excluded_dir(path):
                    log.debug('Skipping excluded directory', path=path, exclusions=self._exclude_dirs)
                    continue

                self.add_header_recursively(path, header_text)
            else:
                if self._is_excluded_file(path):
                    log.debug('Skipping excluded file', path=path, exclusions=self._exclude_files)
                    continue
                self._add_header(path, header_text)

    def _add_header(self, file_path: str, header_text: str) -> None:
        if language := self._language_detector.detect(file_path):
            for exclusion in language.file_exclusions:
                if self._is_matching(exclusion, file_path):
                    log.debug('Skipping excluded file', path=file_path, exclusions=language.file_exclusions)
                    return

            log.debug('Processing file', path=file_path, language=language.name)
            self._header_inserter.insert(file_path, header_text, language)

    def _is_excluded_dir(self, path: str) -> bool:
        for exclusion in self._exclude_dirs:
            if self._is_matching(exclusion, path):
                return True
        return False

    def _is_excluded_file(self, path: str) -> bool:
        for exclusion in self._exclude_files:
            if self._is_matching(exclusion, path):
                return True
        return False

    def _is_matching(self, wildcard_pattern: str, path: str) -> Optional[re.Match[str]]:
        wildcard_pattern = f'^{wildcard_pattern}$'
        pattern = re.compile(wildcard_pattern.replace('.', '\\.').replace('*', '.*'))
        return pattern.match(os.path.basename(path))
