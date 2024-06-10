import unittest
from unittest import TestCase

from context_logger import setup_logging

from header_adder import ConfigLoader
from tests import TEST_RESOURCE_ROOT, TEST_FILE_SYSTEM_ROOT


class ConfigLoaderTest(TestCase):

    @classmethod
    def setUpClass(cls):
        setup_logging('header-adder', 'DEBUG', warn_on_overwrite=False)

    def setUp(self):
        print()

    def test_configuration_loaded_when_file_exists(self):
        # Given
        config_file = f'{TEST_RESOURCE_ROOT}/config/header-adder.conf'
        arguments = {
            'config_file': config_file,
            'exclude_dirs': 'dir3',
            'context': ['year=2025']
        }
        configuration_loader = ConfigLoader(TEST_RESOURCE_ROOT)

        # When
        configuration = configuration_loader.load(arguments)

        # Then
        self.assertEqual('info', configuration['log_level'])
        self.assertEqual(['dir3'], configuration['exclude_dirs'])
        self.assertEqual('2025', configuration['context']['year'])
        self.assertEqual('John Doe', configuration['context']['authors'][0]['name'])
        self.assertEqual('symbol1', configuration['languages']['Language1']['comment_symbol'])
        self.assertEqual('symbol2', configuration['languages']['Language2']['comment_symbol'])

    def test_configuration_loaded_when_file_not_exists(self):
        # Given
        arguments = {'config_file': f'{TEST_FILE_SYSTEM_ROOT}/etc/header-adder.conf'}
        configuration_loader = ConfigLoader(TEST_RESOURCE_ROOT)

        # When
        configuration = configuration_loader.load(arguments)

        # Then
        self.assertEqual('info', configuration['log_level'])
        self.assertEqual(['dir1', 'dir2'], configuration['exclude_dirs'])
        self.assertEqual('2024', configuration['context']['year'])
        self.assertEqual('Jane Doe', configuration['context']['authors'][1]['name'])
        self.assertEqual('.ext1 .ext2', configuration['languages']['Language1']['file_extensions'])
        self.assertEqual('.ext3 .ext4', configuration['languages']['Language2']['file_extensions'])


if __name__ == '__main__':
    unittest.main()
