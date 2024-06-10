import unittest
from unittest import TestCase

from context_logger import setup_logging

from header_adder import HeaderLoader
from tests import TEST_RESOURCE_ROOT, compare_lines


class HeaderLoaderTest(TestCase):

    @classmethod
    def setUpClass(cls):
        setup_logging('header-adder', 'DEBUG', warn_on_overwrite=False)

    def setUp(self):
        print()

    def test_load_without_context(self):
        # Given
        header_loader = HeaderLoader()

        # When
        result = header_loader.load(f'{TEST_RESOURCE_ROOT}/template/header.j2')

        # Then
        expected = 'SPDX-License-Identifier: MIT\n'
        self.assertTrue(compare_lines(expected.splitlines(), result.splitlines()))

    def test_load_with_context(self):
        # Given
        header_loader = HeaderLoader()

        # When
        context = {
            'authors': [
                {'year': '2019', 'name': 'John Doe', 'email': 'john@example.com'},
                {'year': '2020', 'name': 'Jane Doe', 'email': 'jane@example.com'}]
        }
        result = header_loader.load(f'{TEST_RESOURCE_ROOT}/template/header.j2', context)

        # Then
        expected = ('SPDX-FileCopyrightText: 2019 John Doe <john@example.com>\n'
                    'SPDX-FileCopyrightText: 2020 Jane Doe <jane@example.com>\n'
                    'SPDX-License-Identifier: MIT\n')
        self.assertTrue(compare_lines(expected.splitlines(), result.splitlines()))


if __name__ == '__main__':
    unittest.main()
