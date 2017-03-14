import json
import requests
import pickle

# Show a simple message.
print("Welcome to My Lyric Finder.")
print("This is a simple application to search, view and save song lyrics.")


def search_song():

    track_name = input("Enter the Song title:")
    api_key = "fede23bab51e23e61888932cd118ca2c"

    response = requests.get("http://api.musixmatch.com/ws/1.1/track.search",
                            params={
                            'apikey': api_key,
                            'page_size': 10,
                            'page': 1,
                            's_track_rating': 'desc',
                            'q_track': track_name,
                            })
    try:
        response_data = response.json()
        message = response_data.get('message')
        body = message.get('body')
        tracklists = body.get('track_list')
        for t in tracklists:
            t = t.get('track')
            print('track name {}'.format(t.get('track_name')))
            print('track id {}'.format(t.get('track_id')))
            print('lyrics id {}'.format(t.get('lyrics_id')))
            print('artist_mbid {}'.format(t.get('artist_mbid')))
            print('artist_id {}'.format(t.get('artist_id')))
            print('artist_name {}'.format(t.get('artist_name')))
            print('')
    except json.decoder.JSONDecodeError:
        print("Cannot Decode JSON")


def view_lyrics():

    print("Use the artist id from your song choice to get the song lyrics.")
    track_id = input ( "Enter the Track ID from the above results: " )

api_key = "fede23bab51e23e61888932cd118ca2c"

response = requests.get ( "https://api.musixmatch.com/ws/1.1/track.lyrics.get?track_id="+track_id+"&apikey="+api_key)
try:
    response_data = response.json()
    message = response_data.get('message')
    body = message.get('body')
    lyrics = body.get('lyrics')
    lyricsid = lyrics.get('lyric_id')
    for l in lyricsid:
        l = l.get('lyrics_body')
        print('Lyrics {}'.format(t.get('lyrics_body')))
        print('')
    # print(json.dumps(response_data, sort_keys=True, indent=4))
except json.decoder.JSONDecodeError:
    print("Cannot Decode JSON")

search_song()
view_lyrics()