# SPDX-FileCopyrightText: 2024 Ferenc Nandor Janky <ferenj@effective-range.com>
# SPDX-FileCopyrightText: 2024 Attila Gombos <attila.gombos@effective-range.com>
# SPDX-License-Identifier: MIT

from typing import Optional, Any


class Language(object):

    def __init__(self, language_name: str, file_extensions: list[str], file_exclusions: list[str], comment_symbol: str,
                 shebang_pattern: Optional[str]) -> None:
        self.name = language_name
        self.file_extensions = file_extensions
        self.file_exclusions = file_exclusions
        self.comment_symbol = comment_symbol
        self.shebang_pattern = shebang_pattern


class ILanguageLoader(object):

    def load(self, languages: dict[str, Any]) -> list[Language]:
        raise NotImplementedError()


class LanguageLoader(ILanguageLoader):

    def load(self, configuration: dict[str, Any]) -> list[Language]:
        languages = []

        for language_name, language_data in configuration.items():
            file_extensions = self._split_to_list(language_data['file_extensions'])
            file_exclusions = self._split_to_list(language_data.get('file_exclusions', ''))

            language = Language(language_name, file_extensions, file_exclusions,
                                language_data['comment_symbol'], language_data.get('shebang_pattern'))

            languages.append(language)

        return languages

    def _split_to_list(self, string: str) -> list[str]:
        return string.strip(' ').replace('  ', ' ').split(' ') if string else []
