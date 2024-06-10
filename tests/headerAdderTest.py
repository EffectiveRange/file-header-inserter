import unittest
from unittest import TestCase, mock
from unittest.mock import MagicMock

from context_logger import setup_logging

from header_adder import HeaderAdder, ILanguageDetector, HeaderInserter, Language
from tests import TEST_FILE_SYSTEM_ROOT


class HeaderAdderTest(TestCase):

    @classmethod
    def setUpClass(cls):
        setup_logging('header-adder', 'DEBUG', warn_on_overwrite=False)

    def setUp(self):
        print()

    def test_add_header_recursively(self):
        # Given
        language, language_detector, header_inserter, exclude_dirs, exclude_files = create_components()
        header_adder = HeaderAdder(language_detector, header_inserter, exclude_dirs, exclude_files)
        header = 'text'

        # When
        header_adder.add_header_recursively(f'{TEST_FILE_SYSTEM_ROOT}/language1', header)

        # Then
        header_inserter.insert.assert_has_calls([
            mock.call(f'{TEST_FILE_SYSTEM_ROOT}/language1/file1', header, language),
            mock.call(f'{TEST_FILE_SYSTEM_ROOT}/language1/file2.ext2', header, language),
            mock.call(f'{TEST_FILE_SYSTEM_ROOT}/language1/dir1/file2.ext1', header, language)
        ], any_order=True)


def create_components():
    language = Language('Language1', ['.ext1', '.ext2'], ['file1.*', 'file2'], 'symbol1', '^#!shebang1')
    language_detector = MagicMock(spec=ILanguageDetector)
    language_detector.detect.return_value = language
    header_inserter = MagicMock(spec=HeaderInserter)
    exclude_dirs = ['test*']
    exclude_files = ['.*']
    return language, language_detector, header_inserter, exclude_dirs, exclude_files


if __name__ == '__main__':
    unittest.main()
