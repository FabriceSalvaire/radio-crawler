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

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from ..SqlAlchemyBase import SqlRow

####################################################################################################

class PlaylistRowMixin(SqlRow):

    __tablename__ = 'playlist'

    # Record ID
    id = Column(Integer, primary_key=True) # auto-incremented

    radio = Column(Integer, nullable=False) # Fixme:
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)

    ##############################################

    @declared_attr
    def song_id(cls):
        return Column(Integer, ForeignKey('songs.id'))

    @declared_attr
    def song(cls):
        return relationship('SongRow', back_populates='diffusion')

    ##############################################

    def __repr__(self):
        return '{0.radio} | {0.start} — {0.end} | {0.duration} | {0.song_id}'.format(self)

    ##############################################

    @property
    def duration(self):
        return self.end - self.start
