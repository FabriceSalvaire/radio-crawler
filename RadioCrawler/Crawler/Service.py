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

__all__ = ['CrawlerService']

####################################################################################################

import datetime
import logging
import time
import traceback

import requests

from sqlalchemy.orm.exc import NoResultFound

from RadioCrawler.Database import CrawlerDatabase
from RadioCrawler.Database.CrawlerDatabase.SongTable import SongHashMixin

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Song(SongHashMixin):

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

        self.album = kwargs.get('titreAlbum', '')
        self.authors = kwargs.get('authors', '')
        self.label = kwargs.get('label', '')
        self.title = kwargs.get('title', '')
        self.year = int(kwargs.get('anneeEditionMusique', 0))

        self.cover = kwargs.get('visual', None)
        self.youtube = kwargs.get('lienYoutube', None)
        self.youtube_cover = kwargs.get('visuelYoutube', None)

        now = time.time()
        self.start = kwargs.get('start', now)
        self.end = kwargs.get('end', now)

        func = datetime.datetime.fromtimestamp
        self.start_date, self.end_date = [func(x) for x in (self.start, self.end)]

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

    def to_dict(self):
        return {key:getattr(self, key) for key in self.FIELDS}

####################################################################################################

class CrawlerService:

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

    _logger = _module_logger.getChild('Crawler')

    ##############################################

    def __init__(self, config):

        self._config = config

        self._database = CrawlerDatabase.open_database(self._config.Database)
        self._song_table = self._database.song_table
        self._playlist_table = self._database.playlist_table

        self._get_last_song()

        self._running = False
        self._must_exit = False
        self._sleeping = False

    ##############################################

    @property
    def sleeping(self):
        return self._sleeping

    ##############################################

    def stop(self):
        self._running = False
        self._must_exit = True

    ##############################################

    def _get_last_song(self):

        PlaylistRow = self._playlist_table.ROW_CLASS
        last_played_song = self._playlist_table.query().order_by(PlaylistRow.id.desc()).first()
        if last_played_song:
            song_row = last_played_song.song
            self._last_song = Song(**song_row.to_dict())
            self._logger.info('last song {}'.format(self._last_song))
        else:
            self._last_song = None

    ##############################################

    def _add_song(self, song):

        try:
            song_row = self._song_table.filter_by(id=hash(song)).one() # or .one_or_none()
        except NoResultFound:
            song_row = self._song_table.add_new_row(
                # **song.to_dict()
                # uuid=hash(song),
                uuid=song.sha,
                title=song.title,
                authors=song.authors,
                year=song.year,
                album=song.album,
                label=song.label,
                cover=song.cover,
                youtube=song.youtube,
                youtube_cover=song.youtube_cover,
            )

        self._playlist_table.add_new_row(
            radio=self._config.Crawler.radio,
            start=song.start_date,
            end=song.end_date,
            song=song_row,
        )

    ##############################################

    def _poll(self):

        url = self._config.Crawler.url()
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()

        new_songs = [Song(**item) for item in data['steps'].values()]

        if self._last_song:
            last_id = self._last_song.id
            song_ids = [song.id for song in new_songs]
            self._logger.info('\n{}\n{}'.format(last_id, song_ids))
            try:
                index = song_ids.index(last_id)
                new_songs = new_songs[index+1:]
            except ValueError:
                pass

        if new_songs:
            for song in new_songs:
                self._logger.info('\n{}'.format(song))
                self._add_song(song)
            # self._song_table.commit() # implicit
            self._playlist_table.commit()
            self._last_song = new_songs[-1]

    ##############################################

    def run(self):

        self._running = True
        while self._running:
            try: # catch everything
                self._sleeping = False
                self._poll()

                end = self._last_song.end
                duration = (end - time.time()) * self._config.Crawler.poll_scale
                duration -= 5 # for following code
                time_delta = datetime.timedelta(seconds=duration)

                now = datetime.datetime.now()
                next_time = now + time_delta

                # last song | 2019-02-20 13:09:08.795817 | 2019-02-20 13:09:08.795817 | 0:00:00 |
                # Next in -1 day, 23:59:54.953315  @ 2019-02-20 13:09:03.819188  for 2019-02-20 13:09:08.795817
                if duration > 0:
                    logger = self._logger.info
                else:
                    logger = self._logger.warning
                logger('Next in {}  @ {}  for {}'.format(time_delta, next_time, self._last_song.end_date))

                if self._must_exit:
                    break
                self._sleeping = True
                if duration > 0:
                    time.sleep(duration) # s
                else:
                    time.sleep(30) # s

            except Exception as exception:
                message = '\n' + str(exception) + '\n' + traceback.format_exc()
                self._logger.error(message)
                if self._must_exit:
                    break
                self._sleeping = True
                time.sleep(60) # s

        self._logger.info('Exit')
