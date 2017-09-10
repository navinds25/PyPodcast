"""
Model for Pypod
Contains:
1. Model Class for Sql Backend (default=sqlite)
2. 
"""
from sqlalchemy import MetaData,Table,Column,Text
from sqlalchemy.sql import select
import feedparser
import logging
import sys
import os.path
import requests

class PypodModel(object):
    """ Model Class for Sql Backend (default=sqlite)"""
    def __init__(self):
        """ Add options for different backends """
        self.metadata = MetaData('sqlite:///pypodcast.db')
        self.init_tables()
        self.create_tables()
        self.logging = logging
        self.logging.basicConfig(filename='pypod.log', level=logging.DEBUG)

    def init_tables(self):
        """ Table Configuration """
        self.podcast_list = Table(
        'podcast_list', self.metadata,
        Column('podcast_name', Text, primary_key=True),
        Column('podcast_url', Text, primary_key=True))

    def create_tables(self):
        """ Creates Tables -for first time run only """
        self.metadata.create_all()

    def insert_podcast_list(self, pn, pu):
        """Insert's podcast_name and podcast_url in podcast_list table.
        Use with: Pypod_Model.insert_podcast_list(podcast_name, podcast_url)
        """
        self.podcast_list.insert().execute(podcast_name=pn, podcast_url=pu)

    def get_podcast_list(self):
        result_exec = self.podcast_list.select().execute()
        results = result_exec.fetchall()
        return results

    def get_podcast(self, pod_name):
        results_exec = select([self.podcast_list]).where(self.podcast_list.c.podcast_name == pod_name).execute()
        results = results_exec.fetchone()
        name, pod_url = results
        metadata = feedparser.parse(pod_url)
        episodes = {}
        for data in metadata['entries']:
            key = data['title'].replace('#','').replace(' ', '_')
            for d in data['links']:
                if d['type'] == 'audio/mpeg':
                    value = d['href'].rstrip('\r\n')
                    episodes[key] = value
        return episodes

    @staticmethod
    def write_media(url, episode_name):
        r = requests.get(url.strip(), stream=True)
        with open('{}.mp3'.format(episode_name), 'wb') as f:
            for chunk in r.iter_content(chunk_size=512**2):
                f.write(chunk)


if __name__ == '__main__':
    PypodModel().create_tables()
