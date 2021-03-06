# Web cammunications
import urllib3
import urllib3.contrib.pyopenssl
# Authentication cammunications
import certifi
# PYTHON AND SPOTIFY GET IT?
import spotipy
# why not make life easy?
import spotipy.util as util
# this is for something... let us try without it
# import sys
# This is for parsing the json from THE GENIE OF TUNES!
import json
# Sleep function

from datetime import datetime, date, timedelta
import time

# PRINT IT ALL PRETTY
import pprint

urllib3.contrib.pyopenssl.inject_into_urllib3()

http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED', # Force certificate check.
    ca_certs=certifi.where(),  # Path to the Certifi bundle.
)

# You're ready to make verified HTTPS requests.
try:
    r = http.request('GET', 'https://example.com/')
except urllib3.exceptions.SSLError as e:
    # Handle incorrect certificate error.
    print('this r bad exception')

# Testing with my username from a .conf file so y'all don't see it
uname_path = 'uname.conf'
uname_file = open(uname_path)
uname = uname_file.read()
uname = uname.splitlines()[0]
print 'Spotify Username: ' + uname

# won't work for now, needs to actually redirect
## Testing writing my own spotify URL
#spotify_scopes = 'user-modify-public'
#spotify_login_url = 'https://accounts.spotify.com/authorize' + '?response_type=code'
#spotify_login_url = spotify_login_url + '&client_id=' + my_client_id
#spotify_login_url = spotify_login_url + '&client_id=' + my_client_id
#spotify_login_url = spotify_login_url + 


## print user info
#sp = spotipy.Spotify()
#sp.trace = True
#user = sp.user(uname)
#pprint.pprint(user)

brand = 'wbru'

# Contact TuneGenie
# getTopHits
# Adapted version of the code from here:
# https://github.com/colinodell/tunegenie-spotify/blob/master/lib/tunegenie.coffee
# url = 'http://' + brand + '.tunegenie.com/api/v1/brand/tophits'
# referer = 'http://' + brand + '.tunegenie.com/tophits'

now = datetime.now()
timezone_offset = timedelta(hours=4)
now = (now - timezone_offset)
tunegenie_songs = []

# FIXME: Need to fix pytz package install
for i in range(0,23):
    hours = timedelta(hours=i)
    now = now - hours
    start_str = now.strftime("%Y-%m-%dT%H:00:00-04:00")
    print("Start time: " + start_str)
    end_str = now.strftime("%Y-%m-%dT%H:59:59-04:00")
    print("End time: " + end_str)
    url = "http://" + brand + ".tunegenie.com/api/v1/brand/nowplaying/?hour=" + str(now.hour) + "&since=" + start_str + "&until=" + end_str
    print("url: " + url)
    referer = 'http://' + brand + '.tunegenie.com/onair'
    request = http.request('GET', url, fields=None, headers={'referer': referer})
    tunegenie_songs.extend(json.loads(request.data)['response'])
    #for d in json.loads(request.data)['response']:
    #    print("testing")
    #    tunegenie_songs.append(d)
    #    pprint.pprint(tunegenie_songs)



print "Request status: " + str(request.status)
pprint.pprint(tunegenie_songs)
#for d in tunegenie_songs:
#    pprint.pprint(d)
#doRequest url, "http://#{@brand}.tunegenie.com/onair/"
# getLast24Hrs
i = 0

#for i in range(24):
    


#quit()

# print(request.data)
#json_data = request.data

# Now we need to process this JSON data that we have gotten
# pprint.pprint(json.loads(json_data))

#json_decoded = json.loads(json_data)

#print type(json_decoded)

## The return type of json.loads() is a 'dictionary'
## Within that dictionary 'response' contains all the data we want
## within the 'response' dictionary lie dicts of each track
## 'song' and 'title' give you in formation you are looking for
#num = 0
#for s in json_decoded['response']:
#    print num
#    num = num + 1
#    pprint.pprint(s)
#    print s['artist']
#    print s['song']

#sp = spotipy.Spotify()

# Define just what it is about the user's account we need to access
scope = 'playlist-modify-public'

# Login the user so we can start stuff
token = util.prompt_for_user_token(uname, scope)


if token:
    print('User successfully logged in')
    while True:
        playlist_type = int(raw_input('Enter 1 for last 24 hour playlist and 2 for top 40!'))
        print type(playlist_type)
        print playlist_type
        if 1 == playlist_type:
            top_hits = False
            break
        if 2 == playlist_type:
            top_hits = True
            break
        print('You entered an invalid number, try again!')
    playlist_name = raw_input('Enter a name for your WBRU playlist: ')
    print('User authenticated successfully!')
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    playlists = sp.user_playlist_create(uname, playlist_name)
    print('Playlist creation results: ')
    pprint.pprint(playlists)
    playlist_id = playlists['id']
    track_ids = []
    #for s in json_decoded['response']:
    i = 0
    for s in tunegenie_songs:
        try:
            results = sp.search(q=(s['artist'] + ' ' + s['song']), limit=1)
        except:
            print("error finding song:", s['artist'], " ", s['song'])
        for r in results['tracks']['items']:
            #pprint.pprint(r)
            print 'Track id: ' + r['id']
            track_ids.append(r['id'])
            for a in r['artists']:
                print 'Artist name: ' + a['name']
            print 'Track name: ' + r['name']
        time.sleep(0.1)
        i = i + 1
        if i >= 90:
            results = sp.user_playlist_add_tracks(uname, playlist_id, track_ids)
            print 'Results of add to playlist: ' + str(results)
            track_ids = []
            i = 0
    results = sp.user_playlist_add_tracks(uname, playlist_id, track_ids)
else:
    print("Can't get token for", uname)
        

# Now to start let us try and search for a song from the dict
# on Spotify!

#results = sp.search(q='raconteurs', limit=20)
# pprint.pprint(results)

#for r in results['tracks']['items']:
#    print 'Track id: ' + r['id']
#    for a in r['artists']:
#        print 'Artist name: ' + a['name']
#    print 'Track name: ' + r['name']


