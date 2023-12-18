###  LogTale - A python logging framework
A simple, easy to use logging framework that builds on top of the built-in logger module.

### Installation
``` bash
pip install logtale
```

### Usage
Simple Usage:
``` python
import logtale.logtale as tale


def main():
    logtale = tale.LogTale("example", "0.0.1", "./example.toml")
    logger = logtale.logger.getChild(__name__)

    logger.debug("test - debug")
    logger.info("test - info")
    logger.warning("test - warning")
    logger.error("test - error")
    logger.critical("test - critical")

if __name__ == "__main__":
    main()
```

Prepend/Postpend text to the log message:
``` python
logger.addFilter(filter.LogFilter(prepend_text="ExamplePrepend"))
logger.addFilter(filter.LogFilter(postpend_text="ExamplePostpend"))
```

### Configuration File
Create a configuration file for logging settings using the `templates/config_template.toml` file as a template.

``` toml
[output.colors]
# Set the colors associated with each debug level.
# Colors are only applied for logs printed to the console.
# The logging color feature can be enabled/disabled in '[output.console]' section.
DEBUG = '\033[1;36m'
INFO = '\033[1;38m'
WARNING = '\033[1;33m'
ERROR = '\033[1;35m'
CRITICAL = '\033[1;31m'

[output.file]
enable = true # enable/disable logging to a .log file (default=true)
level = "DEBUG" # the base log level for logging to a file (default=DEBUG)
path = "logs/" # the directory to create log files in (default=logs/)
format = "(%(asctime)s)[%(name)s][%(levelname)s]::%(message)s" # the log message format to use for file logging
name = "example.log" # the naming scheme of the log file, by default it's '<project_name>_<version>_<timestamp>.log'

[output.console]
enable = true # enable/disable logging to the console (default=true)
level = "DEBUG" # the base log level for logging to the console (default=DEBUG)
format = "[%(levelname)s]::%(message)s" # the log message format to use for console logging
use_colors = true # enable/disable the use of colors for log levels. colors can be customized in '[output.colors]' section.
```

### Examples
Check the `examples` directory for example scripts and configuration files.

``` python
# ./examples/example.py
import logtale.logtale as tale
import logtale.filter as filter


def main():
    logtale = tale.LogTale("example", "0.0.1", "./example.toml")
    logger = logtale.logger.getChild(__name__)
    logger.addFilter(filter.LogFilter(prepend_text="ExamplePrepend"))

    logger.debug("test - debug")
    logger.info("test - info")
    logger.warning("test - warning")
    logger.error("test - error")
    logger.critical("test - critical")

if __name__ == "__main__":
    main()
```

#### Example log console output
![example console output image](./examples/example_console_output.png)

#### Example log file output
![example file output image](./examples/example_file_output.png)
