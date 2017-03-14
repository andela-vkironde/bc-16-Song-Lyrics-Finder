import json
import requests
import sys
import socket

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dbmodel import LyricsStore, Base


#Start the application
mysession = sessionmaker()


engine = create_engine('sqlite:///lyrics.db')
# Bind the engine to the metadata of the Base class 


mysession.configure(bind=engine)

session = mysession()


print("Welcome to My Lyric Finder.")
print("This is a simple application to search, view and save song lyrics.")

def view_lyrics():

    track_id = input ( "Enter the Track ID from the above results: " )
    track_id = track_id
    api_key = "fede23bab51e23e61888932cd118ca2c"
    response = requests.get("https://api.musixmatch.com/ws/1.1/track.lyrics.get?track_id="+track_id+"&apikey="+api_key)
    
    output = json.loads(response.text)
    
    print(output['message']['body']['lyrics']['lyrics_body'])

    save_lyrics()

    def save_lyrics():
        if output== 0:print("No lyrics found")
        else:
            lyrics_found = LyricsStore(song_id, body)
            session.add(lyrics_found)
            session.commit()
            print("Lyrics saved.")
    except socket.timeout:
        print ("Timeout raised and caught")

def clear_lyricstore():
    
   """ song clear - Clear entire local song database."""
    try:
        # Drop all tables then recreate them.
        Base.metadata.drop_all(bind=engine)
        print("Database cleared successfully.")
        Base.metadata.create_all(bind=engine)
    except:
        session.rollback()

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

search_song()
view_lyrics()