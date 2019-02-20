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

"""Define default configuration.

Theses defaults are overridden in the user configuration file via sub-classing instead of monkey
patching.  Consequently if a class depends of another one, refer to it as *ConfigFile_ClassName* so
as to bind to the ConfigFile space, i.e. to the user version.

"""

####################################################################################################

__all__ = [
    'HOME_DIRECTORY',

    'Crawler',
    'Database',
    'Path',
]

####################################################################################################

import os
import pathlib

####################################################################################################

HOME_DIRECTORY = pathlib.Path(os.environ['HOME'])

####################################################################################################

class Path:

    # Fixme: Linux

    CONFIG_DIRECTORY = HOME_DIRECTORY.joinpath('.config', 'radio-crawler')

    # data_directory = ('.local', 'share', 'data', 'radio-crawler')
    DATA_DIRECTORY = HOME_DIRECTORY.joinpath('.local', 'radio-crawler')

    ##############################################

    @classmethod
    def join_config_directory(cls, *args):
        return cls.CONFIG_DIRECTORY.joinpath(*args)

    ##############################################

    @classmethod
    def join_data_directory(cls, *args):
        return cls.DATA_DIRECTORY.joinpath(*args)

    ##############################################

    @classmethod
    def make_user_directory(cls):

        for directory in (
                cls.CONFIG_DIRECTORY,
                cls.DATA_DIRECTORY,
        ):
            if not directory.exists():
                os.mkdir(directory)

####################################################################################################

ConfigFile_Path = Path

####################################################################################################

class Database:

    driver = 'sqlite'
    hostname = None
    user_name = None
    password = None
    database = None
    echo = False

    ##############################################

    @classmethod
    def crawler_database(cls):
        return ConfigFile_Path.join_data_directory('crawler-database.sqlite')

####################################################################################################

class Crawler:

    url_pattern = None
    radio = None
    poll_scale = 2 / 3

    ##############################################

    @classmethod
    def url(cls):
        return cls.url_pattern.format(cls)
