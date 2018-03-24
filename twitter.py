import sys
import json
import random
import hashlib
import subprocess as subproc

try:
    import requests
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    raise ImportError('Modules are missing:\n  requests\n  bs4')
    sys.exit(1)


def download(link):
    link = _request_player(link)
    filename = hashlib.md5(f'{random.random()}'.encode('utf-8')).digest().hex()
    command = f'ffmpeg -loglevel panic -y -i "{link}" -bsf:a aac_adtstoasc -vcodec copy -c copy -crf 50 {filename}.mp4'

    proc = subproc.Popen(command, shell=True)
    print('Downloading...')

    if proc.wait() == 0:
        print(f'Done! File saved in {filename}.mp4')
    else:
        raise Exception(f'Unexpected error: {proc.wait()}')


def _request_player(link):
    """Returns the m3u8 file url."""
    source = requests.get(_request_tweet(link)).content
    soup = BeautifulSoup(source, 'html.parser')
    tag = soup.body.find_all('div', id='playerContainer')[0]
    data = json.loads(tag.get('data-config'))
    return data['video_url']


def _request_tweet(link):
    source = requests.get(link).content
    soup = BeautifulSoup(source, 'html.parser')
    tag = soup.head.find_all('meta', property='og:video:url')[0]
    return tag.get('content')
