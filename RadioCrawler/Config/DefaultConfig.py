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
    'Crawler',
    'Database',
    'Logging',
    'Path',
]

####################################################################################################

class Path:

    config_directory = None
    data_directory = None

    ##############################################

    @classmethod
    def join_config_directory(cls, *args):
        return cls.config_directory.joinpath(*args)

    ##############################################

    @classmethod
    def join_data_directory(cls, *args):
        return cls.data_directory.joinpath(*args)

####################################################################################################

# hack to reset Path
ConfigFile_Path = Path

####################################################################################################

class Logging:

    ##############################################

    @classmethod
    def config_file(cls_file):
        return ConfigFile_Path.join_config_directory('logging.yml')

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
        # # $HOME/.local/radio-crawler/crawler-database.sqlite
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
