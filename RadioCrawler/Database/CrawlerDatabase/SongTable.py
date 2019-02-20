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

__all__ = ['SongHashMixin', 'SongRowMixin']

####################################################################################################

import hashlib

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

from ..SqlAlchemyBase import SqlRow

####################################################################################################

class SongHashMixin:

    ##############################################

    @property
    def hash_string(self):
        return '-'.join((self.album, self.label, self.title, self.authors, str(self.year)))

    ##############################################

    def __hash__(self):
        return hash(self.hash_string)

    ##############################################

    @property
    def sha(self):
        string = self.hash_string.encode('utf-8')
        return hashlib.sha1(string).hexdigest()

####################################################################################################

class SongRowMixin(SqlRow, SongHashMixin):

    __tablename__ = 'songs'

    # Record ID
    id = Column(Integer, primary_key=True)

    uuid = Column(String, nullable=False)

    title = Column(String, nullable=False)
    authors = Column(String, nullable=False)
    year = Column(Integer)

    album = Column(String, nullable=False)
    label = Column(String, nullable=False)

    cover = Column(String)

    youtube = Column(String)
    youtube_cover = Column(String)

    ##############################################

    @declared_attr
    def diffusion(cls):
        return relationship('PlaylistRow', back_populates='song')

    ##############################################

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.id = hash(self)

    ##############################################

    def __repr__(self):
        return '{0.title} {0.authors}'.format(self)
