import shutil
import unittest
from unittest import TestCase

from context_logger import setup_logging

from header_adder import HeaderInserter, Language
from tests import TEST_RESOURCE_ROOT, TEST_FILE_SYSTEM_ROOT, compare_files


class HeaderInserterTest(TestCase):
    SOURCE_FILES_DIR = f'{TEST_FILE_SYSTEM_ROOT}/src'
    EXPECTED_WITH_EXTENSION = f'{TEST_RESOURCE_ROOT}/source/right_header.ext'
    EXPECTED_WITH_SHEBANG = f'{TEST_RESOURCE_ROOT}/source/shebang_right_header'

    @classmethod
    def setUpClass(cls):
        setup_logging('header-adder', 'DEBUG', warn_on_overwrite=False)

    def setUp(self):
        print()
        shutil.rmtree(self.SOURCE_FILES_DIR, ignore_errors=True)
        shutil.copytree(f'{TEST_RESOURCE_ROOT}/source', self.SOURCE_FILES_DIR, dirs_exist_ok=True)

    def test_inserts_header_when_file_is_empty(self):
        # Given
        header = create_header()
        language = create_language()
        header_inserter = HeaderInserter()

        file_path = f'{self.SOURCE_FILES_DIR}/empty.ext'

        # When
        header_inserter.insert(file_path, header, language)

        # Then
        self.assertTrue(compare_files(f'{TEST_RESOURCE_ROOT}/source/only_header.ext', file_path))

    def test_inserts_header_when_there_is_no_header(self):
        # Given
        header = create_header()
        language = create_language()
        header_inserter = HeaderInserter()

        file_path = f'{self.SOURCE_FILES_DIR}/no_header.ext'

        # When
        header_inserter.insert(file_path, header, language)

        # Then
        self.assertTrue(compare_files(self.EXPECTED_WITH_EXTENSION, file_path))

    def test_replaces_header_when_there_is_wrong_header(self):
        # Given
        header = create_header()
        language = create_language()
        header_inserter = HeaderInserter()

        file_path = f'{self.SOURCE_FILES_DIR}/wrong_header.ext'

        # When
        header_inserter.insert(file_path, header, language)

        # Then
        self.assertTrue(compare_files(self.EXPECTED_WITH_EXTENSION, file_path))

    def test_skips_when_there_is_right_header(self):
        # Given
        header = create_header()
        language = create_language()
        header_inserter = HeaderInserter()

        file_path = f'{self.SOURCE_FILES_DIR}/right_header.ext'

        # When
        header_inserter.insert(file_path, header, language)

        # Then
        self.assertTrue(compare_files(self.EXPECTED_WITH_EXTENSION, file_path))

    def test_inserts_header_when_there_is_shebang_and_no_header(self):
        # Given
        header = create_header()
        language = create_language()
        header_inserter = HeaderInserter()

        file_path = f'{self.SOURCE_FILES_DIR}/shebang_no_header'

        # When
        header_inserter.insert(file_path, header, language)

        # Then
        self.assertTrue(compare_files(self.EXPECTED_WITH_SHEBANG, file_path))

    def test_replaces_header_when_there_is_shebang_and_wrong_header(self):
        # Given
        header = create_header()
        language = create_language()
        header_inserter = HeaderInserter()

        file_path = f'{self.SOURCE_FILES_DIR}/shebang_wrong_header'

        # When
        header_inserter.insert(file_path, header, language)

        # Then
        self.assertTrue(compare_files(self.EXPECTED_WITH_SHEBANG, file_path))

    def test_skips_when_there_is_shebang_and_right_header(self):
        # Given
        header = create_header()
        language = create_language()
        header_inserter = HeaderInserter()

        file_path = f'{self.SOURCE_FILES_DIR}/shebang_right_header'

        # When
        header_inserter.insert(file_path, header, language)

        # Then
        self.assertTrue(compare_files(self.EXPECTED_WITH_SHEBANG, file_path))


def create_header():
    return ('Header line 1\n'
            'Header line 2\n'
            'Header line 3\n')


def create_language():
    return Language('Language', ['.ext'], [], '$$', '^#!shebang')


if __name__ == '__main__':
    unittest.main()
