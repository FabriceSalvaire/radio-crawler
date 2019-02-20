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

import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from ..SqlAlchemyBase import SqlRow

####################################################################################################

class LogRowMixin(SqlRow):

    __tablename__ = 'log'

    # Record ID
    id = Column(Integer, primary_key=True) # auto-incremented

    start = Column(DateTime, nullable=False)
    stop = Column(DateTime, nullable=True)

    ##############################################

    def __init__(self):

        super().__init__()
        self.start = datetime.datetime.now()

    ##############################################

    def set_stop(self):
        self.stop = datetime.datetime.now()

    ##############################################

    def __repr__(self):
        return '{0.start} — {0.stop}'.format(self)
