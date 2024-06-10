# header-adder

Recursively inserts header text into specific files in a directory tree. Useful to add copyright headers to source
files.

## Features

- [x] Automatically detects source file language based on file extension or shebang
- [x] Supported languages can be extended by adding new language configurations
- [x] Supports Jinja2 templating for header text
- [x] Supports configuration file for default values
- [x] Supports command line arguments to override default values

Default configuration file is loaded from `config/header-adder.conf`:

```ini
[global]
log_level = info
exclude_dirs = .* __* test* *test
exclude_files = .*

[context]
year = 2024

[language:C++]
file_extensions = .cpp .cxx .cc .c .h .hpp .hxx
file_exclusions = test* *test
comment_symbol = //

[language:Python]
file_extensions = .py
file_exclusions = setup.py __init__.py *Test.py test_*.py *_test.py conftest.py envs.py
comment_symbol = #
shebang_pattern = ^#!.*\bpython

[language:Shell]
file_extensions = .sh
file_exclusions =
comment_symbol = #
shebang_pattern = ^#!.*\b.*sh$
```

Example Jinja template:

```jinja
{% for author in authors %}SPDX-FileCopyrightText: {{author.year}} {{author.name}} <{{author.email}}>
{% endfor %}SPDX-License-Identifier: MIT
```

Example context values:

```ini
[context]
authors = [
   {"year": "2019", "name": "John Doe", "email": "john@example.com"},
   {"year": "2020", "name": "Jane Doe", "email": "jane@example.com"}]
```

Resulting header text:

```
SPDX-FileCopyrightText: 2019 John Doe <john@example.com>
SPDX-FileCopyrightText: 2020 Jane Doe <jane@example.com>
SPDX-License-Identifier: MIT
```

## Requirements

- [Python3](https://www.python.org/downloads/)
- [jinja](https://github.com/pallets/jinja/)

## Installation

### Install from source root directory

```bash
pip install .
```

### Install from source distribution

1. Create source distribution
    ```bash
    pip setup.py sdist
    ```

2. Install from distribution file
    ```bash
    pip install dist/header_adder-1.0.0.tar.gz
    ```

3. Install from GitHub repository
    ```bash
    pip install git+https://github.com/EffectiveRange/header-adder.git@latest
    ```

## Usage

Example usage:

   ```bash
   python3 bin/header-adder.py /path/to/my/source/files --template /path/to/my/header-template.j2
   ```

Command line arguments:

   ```bash
usage: header-adder.py [-h] [--config-file CONFIG_FILE]
                       [--log-level LOG_LEVEL]
                       [--exclude-dirs EXCLUDE_DIRS [EXCLUDE_DIRS ...]]
                       [--template TEMPLATE] [--context CONTEXT [CONTEXT ...]]
                       directory

positional arguments:
  directory             root directory containing source files

optional arguments:
  -h, --help            show this help message and exit
  --config-file CONFIG_FILE
                        configuration file (default: /etc/header-adder.conf)
  --log-level LOG_LEVEL
                        logging level (default: None)
  --exclude-dirs EXCLUDE_DIRS [EXCLUDE_DIRS ...]
                        directory names to exclude, supports wildcards
                        (default: None)
  --template TEMPLATE, -t TEMPLATE
                        file containing the header template (default: None)
  --context CONTEXT [CONTEXT ...]
                        template context values (default: None)
   ```
