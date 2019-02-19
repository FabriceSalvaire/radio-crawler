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

__all__ = ['Crawler']

####################################################################################################

import argparse

from RadioCrawler.Config.ConfigFile import ConfigFile
from RadioCrawler.Database import CrawlerDatabase
from RadioCrawler.Tools.ProgramOption import PathAction

####################################################################################################

class Crawler:

    ##############################################

    def __init__(self):

        self._parse_args()
        self._config = ConfigFile(self._args.config)
        self._document_database = CrawlerDatabase.open_database(self._config.Database)

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

    def run(self):
        pass
