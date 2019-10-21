# Imports
import math

import spotipy
import spotipy.util as util
from credentials import CREDS

# Global variables
CLIENT_ID = CREDS['CLIENT_ID']
CLIENT_SECRET = CREDS['CLIENT_SECRET']
USERNAME = 'will_i_am_i'
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
        if(SCOPE == 'user-read-recently-played'):
            """
            For experimentation purposes.
            """
            results = sp.current_user_recently_played(50)
            tracks = {}
            artists = {}
            for res in results['items']:
                track = res['track']['name']
                if(track in tracks):
                    tracks[track] += 1
                else:
                    tracks[track] = 1
                for r in res['track']['artists']:
                    if(r['name'] in artists):
                        artists[r['name']] += 1
                    else:
                        artists[r['name']] = 1
            tracks = sorted(tracks.items(), key=lambda x: x[1], reverse=True)
            artists = sorted(artists.items(), key=lambda x: x[1], reverse=True)
            print(tracks)
            print()
            print(artists)
        if(SCOPE == 'user-top-read'):
            artists = {}
            final = ''
            results = sp.current_user_top_tracks(50, time_range='short_term')
            for t, res in enumerate(reversed(results['items']), start=1):
                # print(res['name'], '-', ',
                #       '.join([r['name'] for r in res['artists']]),
                #       ':', str(res['popularity'])+'%')
                for r in res['artists']:
                    if(r['name'] in artists):
                        artists[r['name']] += math.log2(t)
                    else:
                        artists[r['name']] = math.log2(t)
            artists = sorted(artists.items(), key=lambda x: (x[1], x[0]),
                             reverse=True)[:10]
            freq = sum(x[1] for x in artists)
            # print('{:<20} {:^20} {:>20}'.format('Artist', 'Percentage bar',
            #                                     'Different songs'))
            for i, j in artists:
                bar = generateBarChart(j/freq, 20)
                # print('{:<20} {:^20} {:>13}'.format(i, bar, j))
                final += '{:<20} {:^20} {:>8.2f}%\n'.format(
                    i, bar, j/freq*100)
            return final
    else:
        return("Can't get token for", USERNAME)
