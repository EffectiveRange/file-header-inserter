# SPDX-FileCopyrightText: 2024 Ferenc Nandor Janky <ferenj@effective-range.com>
# SPDX-FileCopyrightText: 2024 Attila Gombos <attila.gombos@effective-range.com>
# SPDX-License-Identifier: MIT

from context_logger import get_logger

from header_adder import Language

log = get_logger('HeaderInserter')


class IHeaderInserter(object):

    def insert(self, file_path: str, header_text: str, language: Language) -> None:
        raise NotImplementedError()


class HeaderInserter(IHeaderInserter):

    def insert(self, file_path: str, header_text: str, language: Language) -> None:
        with open(file_path, 'r') as file:
            file_lines = file.readlines()

        if not file_lines:
            file_lines = ['\n']

        comment = language.comment_symbol
        shebang = self._is_shebang_present(file_lines)
        header_lines = [f'{comment} {line}\n' for line in header_text.splitlines()]

        if self._is_any_header_present(file_lines, comment, shebang):
            if self._is_matching_header_present(file_lines, header_lines, shebang):
                log.info('Header already present, skipping', file=file_path, language=language.name)
                return
            else:
                log.info('Replacing existing header', file=file_path, language=language.name)
                self._remove_header(file_lines, comment, shebang)
                self._insert_header(file_path, file_lines, header_lines, shebang)
        else:
            log.info('Inserting header', file=file_path, language=language.name)
            self._insert_header(file_path, file_lines, header_lines, shebang)

    def _is_shebang_present(self, file_lines: list[str]) -> bool:
        return file_lines[0].startswith('#!')

    def _is_any_header_present(self, file_lines: list[str], comment: str, shebang: bool) -> bool:
        lines = file_lines[1:] if shebang else file_lines
        for line in lines:
            if line == '\n':
                continue
            return line.startswith(comment)

        return False

    def _is_matching_header_present(self, file_lines: list[str], header_lines: list[str], shebang: bool) -> bool:
        header_length = len(header_lines)
        lines = [line for line in file_lines if line != '\n']
        lines = lines[1:header_length + 1] if shebang else lines[:header_length]
        return lines == header_lines

    def _insert_header(self, file_path: str, file_lines: list[str], header_lines: list[str], shebang: bool) -> None:
        with open(file_path, 'w') as file:
            if shebang:
                file.write(file_lines[0])
                file.write('\n')

            for line in header_lines:
                file.write(line)

            file_lines = file_lines[1:] if shebang else file_lines

            if not file_lines or file_lines[0] != '\n':
                file.write('\n')

            if file_lines and file_lines[0] == '\n':
                file_lines = file_lines[1:]

            for line in file_lines:
                file.write(line)

    def _remove_header(self, file_lines: list[str], comment: str, shebang: bool) -> None:
        start = 1 if shebang else 0
        while len(file_lines) > start and (file_lines[start].startswith(comment) or file_lines[start] == '\n'):
            file_lines.pop(start)
