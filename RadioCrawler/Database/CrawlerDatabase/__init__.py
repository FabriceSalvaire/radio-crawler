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

__all__ = ['open_database']

####################################################################################################

import logging

from sqlalchemy import Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound

from ..ServerDatabase import ServerDatabase
from ..SqlAlchemyBase import SqlTable
from ..SqliteDatabase import SqliteDatabase

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class CrawlerDatabase(SqliteDatabase):

    _logger = _module_logger.getChild('CrawlerDatabase')

    ##############################################

    @classmethod
    def create_schema_classes(cls):

        cls._logger.debug('')

        declarative_base_cls = declarative_base()

        from .PlaylistTable import PlaylistRowMixin
        from .SongTable import SongRowMixin

        song_row_cls = type('SongRow', (SongRowMixin, declarative_base_cls), {})
        song_table_cls = type('SongTable', (SqlTable,), {
            'ROW_CLASS': song_row_cls,
        })

        playlist_row_cls = type('PlaylistRow', (PlaylistRowMixin, declarative_base_cls), {})
        playlist_table_cls = type('PlaylistTable', (SqlTable,), {
            'ROW_CLASS': playlist_row_cls,
        })

        row_classes = dict(
            playlist=playlist_row_cls,
            song=song_row_cls,
        )

        table_classes = dict(
            playlist=playlist_table_cls,
            song=song_table_cls,
        )

        return declarative_base_cls, row_classes, table_classes

    ##############################################

    # def _create_indexes(self, analysis):

    #     indexes = []
    #     if analysis:
    #         length = self._..._row_class.get_column('...')
    #         indexes += (
    #             Index('..._index', length.asc()),
    #             )

    #     for index in indexes:
    #         index.create(self._engine)

####################################################################################################

class CrawlerSqliteDatabase(CrawlerDatabase, SqliteDatabase):

    ##############################################

    def __init__(self, filename, echo=False):

        super().__init__(filename, echo)

        self.init_schema()

        if self.create():
            # self._create_indexes(analysis)
            pass

####################################################################################################

class CrawlerServerDatabase(CrawlerDatabase, ServerDatabase):

    ##############################################

    def __init__(self, database_config, echo=False):

        super().__init__(database_config, echo)

        self.init_schema()

        if self.create():
            # self._create_indexes(analysis)
            pass

####################################################################################################

def open_database(database_config):

    if database_config.DRIVER == 'sqlite':
        return CrawlerSqliteDatabase(database_config.crawler_database())
    else:
        return CrawlerServerDatabase(database_config)
