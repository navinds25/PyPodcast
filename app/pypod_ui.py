""" UI/Controller for Pypodcast """
from bottle import route, run, request, template
import requests
import requests_cache
from pypod_model import PypodModel

@route('/')
def main_page():
    from_db = PypodModel().get_podcast_list()
    output = template('main_page', rows=from_db)
    return output

@route('/new_podcast')
def new_podcast():
    return '''
        <h1> Get a Podcast </h1>
        <form action="/add_podcast" method="post">
            podcast_name: <input name="podcast_name" type="text" />
            podcast_url: <input name="podcast_url" type="text" />
            <input value="Add Podcast" type="submit" />
        </form>
'''

@route('/add_podcast', method='POST')
def add_podcast():
    podcast_name = request.forms.get('podcast_name')
    podcast_url = request.forms.get('podcast_url')
    PypodModel().insert_podcast_list(pn=podcast_name, pu=podcast_url)
    return "Added podcast : {} with url: {} \n".format(podcast_name, podcast_url)

@route('/get_podcast')
@route('/get_podcast/<podcast_name>')
def get_podcast(podcast_name):
    episode_list = PypodModel().get_podcast(podcast_name)
    output = template('get_podcast', podcast_name=podcast_name, episode_list=episode_list)
    return output

@route('/get_episode')
@route('/get_episode/<podcast_name>')
@route('/get_episode/<podcast_name>/<episode_name>')
def get_episode(podcast_name, episode_name):
    episode_list = PypodModel().get_podcast(podcast_name)
    get_url = episode_list[episode_name]
    PypodModel().write_media(get_url, episode_name)
    return "Downloaded file as {}".format(episode_name)

if __name__ == '__main__':
    run(host='127.0.0.1', port=8080, debug=True)
