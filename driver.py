# Imports
import math

import spotipy
import spotipy.util as util
from credentials import CREDS

# Global variables
CLIENT_ID = CREDS['CLIENT_ID']
CLIENT_SECRET = CREDS['CLIENT_SECRET']
USERNAME = 'Your username'
SCOPE = 'user-top-read'  # user-read-recently-played


def generateBarChart(fraction, size):
    syms = " ▏▎▍▌▋▊▉█"

    frac = size * 8 * fraction
    barsFull = frac // 8
    semi = round(frac % 8)
    barsEmpty = size - barsFull - 1

    return('|' + (syms[8] * int(barsFull)) + syms[semi:semi+1] +
           (syms[0] * int(barsEmpty)) + '|')


def main():
    # Token generation
    token = util.prompt_for_user_token(USERNAME, scope=SCOPE,
                                       client_id=CLIENT_ID,
                                       client_secret=CLIENT_SECRET,
                                       redirect_uri='http://localhost/')

    # Driver code
    if token:
        sp = spotipy.Spotify(auth=token)
        artists = {}
        final = ''
        results = sp.current_user_top_tracks(50, time_range='short_term')
        for t, res in enumerate(reversed(results['items']), start=1):
            for r in res['artists']:
                if(r['name'] in artists):
                    artists[r['name']][0] += math.log2(t)
                    artists[r['name']][1] = res['name']
                else:
                    artists[r['name']] = [math.log2(t), res['name']]
        artists = sorted(artists.items(), key=lambda x: (x[1][0], x[0]),
                         reverse=True)[:10]
        freq = sum(x[1][0] for x in artists)
        for i, j in artists:
            bar = generateBarChart(j[0]/freq, 20)
            final += '{:<25} {:<10} {:>10.2f}% {:>35}\n'.format(
                i, bar, j[0]/freq*100, j[1])
        return final
    else:
        return("Can't get token for", USERNAME)
