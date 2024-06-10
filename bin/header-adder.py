# SPDX-FileCopyrightText: 2024 Ferenc Nandor Janky <ferenj@effective-range.com>
# SPDX-FileCopyrightText: 2024 Attila Gombos <attila.gombos@effective-range.com>
# SPDX-License-Identifier: MIT

import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from pathlib import Path
from typing import Any

from context_logger import get_logger, setup_logging

from header_adder import ConfigLoader, LanguageLoader, HeaderAdder, HeaderInserter, LanguageDetector, HeaderLoader

APPLICATION_NAME = 'header-adder'

log = get_logger('HeaderAdderApp')


def main() -> None:
    resource_root = _get_resource_root()
    arguments = _get_arguments()

    setup_logging(APPLICATION_NAME)

    log.info('Started header-adder', arguments=arguments)

    config = ConfigLoader(resource_root).load(arguments)

    _update_logging(config)

    template = config.get('template')

    if not template:
        raise ValueError('No header file provided. Specify file path with --template (-t) option.')

    language_loader = LanguageLoader()
    languages = language_loader.load(config['languages'])
    language_detector = LanguageDetector(languages)
    header_loader = HeaderLoader()
    header_inserter = HeaderInserter()
    header_adder = HeaderAdder(language_detector, header_inserter, config['exclude_dirs'], config['exclude_files'])

    context = config.get('context')
    header_text = header_loader.load(template, context)

    header_adder.add_header_recursively(config['directory'], header_text)


def _get_resource_root() -> str:
    return str(Path(os.path.dirname(__file__)).parent.absolute())


def _get_arguments() -> dict[str, Any]:
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--config-file', help='configuration file', default='/etc/header-adder.conf')
    parser.add_argument('--log-level', help='logging level')
    parser.add_argument('--exclude-dirs', help='directory names to exclude, supports wildcards', nargs='+')
    parser.add_argument('--exclude-files', help='file names to exclude, supports wildcards', nargs='+')

    parser.add_argument('--template', '-t', help='file containing the header template')
    parser.add_argument('--context', help='template context values', nargs='+')
    parser.add_argument('directory', help='root directory containing source files')

    return {k: v for k, v in vars(parser.parse_args()).items() if v is not None}


def _update_logging(configuration: dict[str, Any]) -> None:
    log_level = configuration.get('log_level', 'INFO')
    if log_level != 'INFO':
        setup_logging(APPLICATION_NAME, log_level, warn_on_overwrite=False)


if __name__ == '__main__':
    main()
