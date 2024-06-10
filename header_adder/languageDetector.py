# SPDX-FileCopyrightText: 2024 Ferenc Nandor Janky <ferenj@effective-range.com>
# SPDX-FileCopyrightText: 2024 Attila Gombos <attila.gombos@effective-range.com>
# SPDX-License-Identifier: MIT

import os
import re
from typing import Optional

from context_logger import get_logger

from header_adder import Language

log = get_logger('LanguageDetector')


class ILanguageDetector(object):

    def detect(self, file_path: str) -> Optional[Language]:
        raise NotImplementedError()


class LanguageDetector(ILanguageDetector):

    def __init__(self, languages: list[Language]) -> None:
        self._languages = languages

    def detect(self, file_path: str) -> Optional[Language]:
        if not os.path.isfile(file_path):
            log.error('File does not exist', file=file_path)
            return None

        if language := (self._detect_by_extension(file_path) or self._detect_by_shebang(file_path)):
            return language

        log.error('Failed to detect language', file=file_path, languages=[lang.name for lang in self._languages])
        return None

    def _detect_by_extension(self, file_path: str) -> Optional[Language]:
        if '.' in file_path:
            for language in self._languages:
                if os.path.splitext(file_path)[1] in language.file_extensions:
                    log.debug('Detected language by extension', file=file_path, language=language.name)
                    return language
        return None

    def _detect_by_shebang(self, file_path: str) -> Optional[Language]:
        try:
            with open(file_path, 'r') as file:
                file_lines = file.readlines()
                if len(file_lines) == 0:
                    log.error('Failed to detect language by shebang, file is empty', file=file_path)
                    return None
        except Exception as error:
            log.error('Failed to read file', file=file_path, error=error)
            return None

        first_line = file_lines[0].strip()

        for language in self._languages:
            if language.shebang_pattern is not None:
                pattern = re.compile(language.shebang_pattern)
                if pattern.match(first_line):
                    log.debug('Detected language by shebang', file=file_path, language=language.name,
                              shebang=first_line)
                    return language
        return None
