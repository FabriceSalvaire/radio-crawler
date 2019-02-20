####################################################################################################
#
# RadioCrawler - A Radio Playlist Crawler
# Copyright (C) 2019 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

__all__ = ['CrawlerDaemon']

####################################################################################################

import argparse
import logging
import signal
import sys

from RadioCrawler.Config.ConfigFile import ConfigFile
from RadioCrawler.Logging import Logging
from RadioCrawler.Tools.ProgramOption import PathAction
from .Service import CrawlerService

####################################################################################################

class CrawlerDaemon:

    ##############################################

    def __init__(self):

        self._parse_args()
        self._config = ConfigFile(self._args.config)
        self._set_signal()

        self._logger = Logging.setup_logging(application_name='radio-crawler',
                                             config_file=self._config.Logging.config_file())

        self._logger.info('Started Radio Crawler')
        self._service = CrawlerService(self._config)
        self._service.run()

    ##############################################

    def _parse_args(self):

        parser = argparse.ArgumentParser(
            description='A Radio Crawler',
        )

        parser.add_argument(
            '--config',
            action=PathAction,
            default=None,
            help='config file',
        )

        parser.add_argument(
            '--version',
            action='store_true', default=False,
            help="show version and exit",
        )

        self._args = parser.parse_args()

    ##############################################

    def _set_signal(self):

        signal.signal(signal.SIGUSR1, self._on_kill)
        try:
            signal.signal(signal.SIGSTOP, self._on_kill)
        except OSError:
            pass

    ##############################################

    def _on_kill(self, signum, frame):
        self._logger.info('Received signal {} sleeping {}'.format(signum, self._service.sleeping))
        if self._service.sleeping:
            sys.exit()
        else:
            self._service.stop()
