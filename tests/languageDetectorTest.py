import unittest
from unittest import TestCase

from context_logger import setup_logging

from header_adder import LanguageDetector, Language
from tests import TEST_FILE_SYSTEM_ROOT


class FileLanguageDetectorTest(TestCase):

    @classmethod
    def setUpClass(cls):
        setup_logging('header-adder', 'DEBUG', warn_on_overwrite=False)

    def setUp(self):
        print()

    def test_detect_returns_none_when_file_not_exists(self):
        # Given
        configurations = create_languages()
        detector = LanguageDetector(configurations)

        # When
        result = detector.detect(f'{TEST_FILE_SYSTEM_ROOT}/shebang')

        # Then
        self.assertIsNone(result)

    def test_detect_returns_none_when_detection_fails(self):
        # Given
        configurations = create_languages()
        detector = LanguageDetector(configurations)

        # When
        result = detector.detect(f'{TEST_FILE_SYSTEM_ROOT}/no_language')

        # Then
        self.assertIsNone(result)

    def test_detect_by_extension(self):
        # Given
        configurations = create_languages()
        detector = LanguageDetector(configurations)

        # When
        result = detector.detect(f'{TEST_FILE_SYSTEM_ROOT}/language2/file1.ext3')

        # Then
        self.assertEqual('Language2', result.name)

    def test_detect_by_shebang(self):
        # Given
        configurations = create_languages()
        detector = LanguageDetector(configurations)

        # When
        result = detector.detect(f'{TEST_FILE_SYSTEM_ROOT}/language1/file1')

        # Then
        self.assertEqual('Language1', result.name)


def create_languages():
    return [
        Language('Language1', ['.ext1', '.ext2'], ['file1.ext1', 'file2'], 'symbol1', '^#!shebang1'),
        Language('Language2', ['.ext3', '.ext4'], ['file2.ext4'], 'symbol2', None)
    ]


if __name__ == '__main__':
    unittest.main()
