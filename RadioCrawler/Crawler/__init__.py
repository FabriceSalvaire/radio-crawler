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

# import json
# import pprint

import datetime
import requests
import time

import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

####################################################################################################

Base = declarative_base()

class SongRow(Base):

    # Fixme: merge SongRow and Song

    __tablename__ = 'playlist'

    id = Column(Integer, primary_key=True)
    album = Column(String)
    authors = Column(String)
    cover = Column(String)
    end = Column(Integer)
    label = Column(String)
    start = Column(Integer)
    title = Column(String)
    year = Column(String)
    youtube = Column(String)
    youtube_cover = Column(String)

    ##############################################

    def __repr__(self):
        return '{0.title} {0.authors}'.format(self)

    ##############################################

    def to_song(self):
        kwargs = {key:getattr(self, key) for key in Song.FIELDS}
        return Song(**kwargs)

####################################################################################################

class Song:

    FIELDS = (
        'album',
        'authors',
        'cover',
        'end',
        'label',
        'start',
        'title',
        'year',
        'youtube',
        'youtube_cover',
    )

    ##############################################

    def __init__(self, **kwargs):

        # self.id = kwargs.get('stepId', None)
        self.year = kwargs.get('anneeEditionMusique', None)
        self.authors = kwargs.get('authors', None)
        self.label = kwargs.get('label', None)
        self.youtube = kwargs.get('lienYoutube', None)
        self.title = kwargs.get('title', None)
        self.album = kwargs.get('titreAlbum', None)
        self.cover = kwargs.get('visual', None)
        self.youtube_cover = kwargs.get('visuelYoutube', None)

        self.start = kwargs['start']
        self.end = kwargs['end']
        func = datetime.datetime.fromtimestamp
        self.start_date, self.end_date = [func(kwargs[key]) for key in ('start', 'end')]

    ##############################################

    @property
    def id(self):
        return '___'.join([x.lower() for x in (self.title, self.authors)]).replace(' ', '-')

    @property
    def duration(self):
        delta = self.end - self.start
        return datetime.timedelta(seconds=delta)

    ##############################################

    def __repr__(self):
        return '| {0.start_date} | {0.end_date} | {0.duration} | {0.title} — {0.authors}'.format(self)

    ##############################################

    def to_row(self):
        kwargs = {key:getattr(self, key) for key in self.FIELDS}
        return SongRow(**kwargs)

####################################################################################################

class Crawler:

    KEYS = (
        'anneeEditionMusique',
        'authors',
        # 'composers',
        # 'coverUuid',
        # 'depth',
        # 'discJockey',
        # 'embedId',
        # 'embedType',
        'end',
        # 'fatherStepId',
        'label',
        'lienYoutube',
        # 'path',
        # 'performers',
        # 'releaseId',
        # 'songId', # change ???
        'start',
        # 'stationId',
        # 'stepId',
        'title',
        # 'titleSlug',
        'titreAlbum',
        # 'uuid',
        'visual',
        'visuelYoutube',
    )

    ##############################################

    def __init__(self, sqlite_path, url):

        self._sqlite_path = sqlite_path
        self._url = url

        self._songs = []

        self._engine = sqlalchemy.create_engine('sqlite:///{}'.format(self._sqlite_path), echo=False)
        Base.metadata.create_all(self._engine)
        Session = sessionmaker(bind=self._engine)
        self._session = Session()

        # Fixme: restart need id
        last_song = self._session.query(SongRow).order_by(SongRow.id.desc()).first()
        if last_song:
            last_song = last_song.to_song()
            print('last song', repr(last_song))
            self._songs.append(last_song)

    ##############################################

    def get(self):

        r = requests.get(url)
        data = r.json()

        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(data)

        new_songs = [Song(**item) for item in data['steps'].values()]

        if self._songs:
            last_id = self._songs[-1].id
            song_ids = [song.id for song in new_songs]
            print('\n', last_id, song_ids)
            try:
                index = song_ids.index(last_id)
                new_songs = new_songs[index+1:]
            except ValueError:
                pass

        print()
        for song in new_songs:
            print(repr(song))
            self._session.add(song.to_row())
        self._session.commit()

        self._songs += new_songs

        return self._songs[-1].end

    ##############################################

    def run(self):

        while True:
            print('-'*100)
            end = crawler.get()
            factor = 2 / 3
            duration = (end - time.time()) * factor
            time_delta = datetime.timedelta(seconds=duration)
            now = datetime.datetime.now()
            next_time = now + time_delta
            print()
            print('Next in {}    @ {}'.format(time_delta, next_time))
            # time.sleep(60) # s
            time.sleep(duration) # s

####################################################################################################

sqlite_path = 'db.sqlite3'
url = 'https://www.fip.fr/livemeta/7'

crawler = Crawler(sqlite_path, url)
crawler.run()
