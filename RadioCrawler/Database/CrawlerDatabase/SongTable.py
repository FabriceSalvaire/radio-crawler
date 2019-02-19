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

####################################################################################################

from sqlalchemy import Column, Integer, String, DateTime

####################################################################################################

from ..SqlAlchemyBase import SqlRow

####################################################################################################

class SongRowMixin(SqlRow):

    __tablename__ = 'songs'

    # Record ID
    id = Column(Integer, primary_key=True)

    title = Column(String)
    authors = Column(String)
    year = Column(String)

    album = Column(String)
    label = Column(String)

    cover = Column(String)

    youtube = Column(String)
    youtube_cover = Column(String)

    ##############################################

    def __repr__(self):
        return '{0.title} {0.authors}'.format(self)
