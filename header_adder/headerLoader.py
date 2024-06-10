# SPDX-FileCopyrightText: 2024 Ferenc Nandor Janky <ferenj@effective-range.com>
# SPDX-FileCopyrightText: 2024 Attila Gombos <attila.gombos@effective-range.com>
# SPDX-License-Identifier: MIT

import os
from typing import Optional, Any

from jinja2 import Environment, FileSystemLoader


class IHeaderLoader(object):

    def load(self, template_path: str, context: Optional[dict[str, Any]] = None) -> str:
        raise NotImplementedError()


class HeaderLoader(IHeaderLoader):

    def load(self, template_path: str, context: Optional[dict[str, Any]] = None) -> str:
        context = context or {}
        environment = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))
        template = environment.get_template(os.path.basename(template_path))
        return f'{template.render(context)}\n'
