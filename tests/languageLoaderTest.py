import unittest
from unittest import TestCase

from context_logger import setup_logging

from header_adder import LanguageLoader


class LanguageLoaderTest(TestCase):

    @classmethod
    def setUpClass(cls):
        setup_logging('header-adder', 'DEBUG', warn_on_overwrite=False)

    def setUp(self):
        print()

    def test_load(self):
        # Given
        language_loader = LanguageLoader()

        # When
        result = language_loader.load({
            'Language1': {
                'file_extensions': '.ext1 .ext2',
                'file_exclusions': 'file1.ext1 file2',
                'comment_symbol': 'symbol1',
                'shebang_pattern': '^#!shebang1'
            },
            'Language2': {
                'file_extensions': '.ext3 .ext4',
                'file_exclusions': 'file2.ext4',
                'comment_symbol': 'symbol2'
            }
        })

        # Then
        self.assertEqual(2, len(result))
        self.assertEqual('Language1', result[0].name)
        self.assertEqual(['.ext1', '.ext2'], result[0].file_extensions)
        self.assertEqual(['file1.ext1', 'file2'], result[0].file_exclusions)
        self.assertEqual('symbol1', result[0].comment_symbol)
        self.assertEqual('^#!shebang1', result[0].shebang_pattern)
        self.assertEqual('Language2', result[1].name)
        self.assertEqual(['.ext3', '.ext4'], result[1].file_extensions)
        self.assertEqual(['file2.ext4'], result[1].file_exclusions)
        self.assertEqual('symbol2', result[1].comment_symbol)


if __name__ == '__main__':
    unittest.main()
