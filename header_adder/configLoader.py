# SPDX-FileCopyrightText: 2024 Ferenc Nandor Janky <ferenj@effective-range.com>
# SPDX-FileCopyrightText: 2024 Attila Gombos <attila.gombos@effective-range.com>
# SPDX-License-Identifier: MIT

import json
import os
import shutil
from configparser import ConfigParser
from pathlib import Path
from typing import Any

from context_logger import get_logger

log = get_logger('ConfigLoader')


class IConfigLoader(object):

    def load(self, arguments: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError()


class ConfigLoader(IConfigLoader):

    def __init__(self, resource_root: str):
        self._resource_root = resource_root

    def load(self, arguments: dict[str, Any]) -> dict[str, Any]:
        config_file = Path(arguments['config_file'])

        if not os.path.exists(config_file):
            log.info('Loading default configuration file', config_file=str(config_file))
            default_config = f'{self._resource_root}/config/header-adder.conf'
            config_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(default_config, config_file)
        else:
            log.info('Using configuration file', config_file=str(config_file))

        parser = ConfigParser()
        parser.read(config_file)

        configuration: dict[str, Any] = dict(parser['global'])
        configuration.update(arguments)

        configuration['exclude_dirs'] = self._split_to_list(configuration.get('exclude_dirs'))
        configuration['exclude_files'] = self._split_to_list(configuration.get('exclude_files'))

        configuration['context'] = self._merge_context(parser, arguments)
        configuration['languages'] = self._get_languages(parser)

        return configuration

    def _split_to_list(self, string: Any) -> list[str]:
        return str(string).strip(' ').replace('  ', ' ').split(' ') if string else []

    def _merge_context(self, parser: ConfigParser, arguments: dict[str, Any]) -> dict[str, Any]:
        context = dict(parser['context'])

        if 'context' in arguments:
            for item in arguments['context']:
                item = item.split('=')
                context[item[0]] = item[1]

        for item in context:
            if context[item].startswith('[') or context[item].startswith('{'):
                context[item] = json.loads(context[item])

        return context

    def _get_languages(self, parser: ConfigParser) -> dict[str, dict[str, str]]:
        languages = dict()

        for section in parser.sections():
            if section.startswith('language:'):
                language = section.split(':')[1]
                languages[language] = dict(parser[section])

        return languages
