####################################################################################################
#
# RadioCrawler - A Radio Playlist Crawler
# Copyright (C) 2019 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
####################################################################################################

__all__ = ['setup_logging']

####################################################################################################

import logging
import logging.config
import os

import yaml

import RadioCrawler.Config.ConfigInstall as ConfigInstall
default_config_file = ConfigInstall.Logging.default_config_file()

####################################################################################################

def setup_logging(application_name='RadioCrawler',
                  config_file=default_config_file):

    logging_config = yaml.load(open(str(config_file), 'r'))

    if ConfigInstall.OS.on_linux:
        # Fixme: \033 is not interpreted in YAML
        formatter_config = logging_config['formatters']['ansi']['format']
        logging_config['formatters']['ansi']['format'] = formatter_config.replace('<ESC>', '\033')

    if ConfigInstall.OS.on_windows:
        formatter = 'simple'
    else:
        formatter = 'ansi'
    logging_config['handlers']['console']['formatter'] = formatter

    logging.config.dictConfig(logging_config)

    logger = logging.getLogger(application_name)
    log_level_env = 'RadioCrawlerLogLevel'
    if log_level_env in os.environ:
        numeric_level = getattr(logging, os.environ[log_level_env], None)
        logger.setLevel(numeric_level)

    return logger
