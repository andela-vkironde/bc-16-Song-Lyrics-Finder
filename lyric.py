import json
import requests
import sys
import cmd

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from docopt import docopt, DocoptExit 
from colorama import init, Fore 
init() 
from pyfiglet import Figlet
from termcolor import colored  #Print my welcoming instruction in colour
from tabulate import tabulate #not used yet

from dbmodel import LyricsStore, Base


#Start the session
mysession = sessionmaker()


engine = create_engine('sqlite:///lyrics.db')
# Bind the engine to the metadata of the Base class 


mysession.configure(bind=engine)

session = mysession()

#Function to view my lyrics
def view_lyrics():
    """view <song_id> - View song lyrics based on its ID. Optimized to check for local copy first."""
    track_id = input ( "Enter the Track ID from the above results: " )
    api_key = "fede23bab51e23e61888932cd118ca2c"
    response = requests.get("https://api.musixmatch.com/ws/1.1/track.lyrics.get?track_id="+track_id+"&apikey="+api_key)
    
    output = json.loads(response.text)
    
    print(output['message']['body']['lyrics']['lyrics_body'])

    #Function to save the lyrics
    def save_lyrics(track_id):
        """save <song_id> - store song details and lyrics locally"""
        try:
            if output== 0:
                print("No lyrics found")
            else:
                song_id = track_id
                song_lyrics = output

                lyrics_found = LyricsStore(song_id, json.dumps(song_lyrics))
                session.add(lyrics_found)
                session.commit()
                print("Lyrics saved.")
                print("                                                                      ")
                print("                                                                      ")
                print("That was fun :)")

                choice2 = input("Would you like to search for something else? Enter Y/N")

                if choice2=="Y":
                    #Search another song
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
                        try:  #This decoded the JSON
                            response_data = response.json()
                            message = response_data.get('message')
                            body = message.get('body')
                            tracklists = body.get('track_list')
                            for t in tracklists:
                                t = t.get('track')
                                print('track name {}'.format(t.get('track_name')))
                                print('track id {}'.format(t.get('track_id')))
                                print('lyrics id {}'.format(t.get('lyrics_id')))
                                print('artist_id {}'.format(t.get('artist_id')))
                                print('artist_name {}'.format(t.get('artist_name')))
                                print('')
                        except json.decoder.JSONDecodeError:
                            print("Cannot Decode JSON")
                    search_song()
                    view_lyrics()

                else: #Stop the song search
                    print("Goodbye.")
        except socket.timeout:
            print ("Timeout raised and caught")

    save_lyrics(track_id)

def clear_lyricstore():
    """ song clear - Clear entire local song database."""

    choice1=input("Are you sure about this? Enter Y/N")
    if choice1 == "Y":
        Base.metadata.drop_all(bind=engine)
        print("Database cleared successfully.")
        Base.metadata.create_all(bind=engine)
    else:
        print("Good Choice!")
        session.rollback() # Drop all tables then recreate them
#Engage the user in choice
def menu():
    print("\n[1] Search for a song.")
    print("\n[2] Clear local song database.")
    print("\n[q] Quit.")

    choice=input("What can I help you do?")

    if choice == "1":
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

    elif choice == "2":
        clear_lyricstore()
    elif choice == "q":
        print("\nI thought you were serious about this man! Bye.")
        quit()
        
    else:
        print("\nComeon!That's not in the choices.\n")
        print("\nLet's try that again.\n")
        menu()

#Brighten up my interface using termcolor
class LyricsStore (cmd.Cmd):
    print(colored(".-." * 30,"white"))
    print(colored(Figlet(font='slant').renderText('\t      K A R A B L E'),"white"))
    print(colored(".-." * 30,"white"))
    print(colored("\t\t\t     The Karaoke Bible. ","white"))
    print(colored(" \t           To use at every singing opportunity.","white"))
    print("                                                                    ")
    print(colored(" \t                        Seriously.","white"))
    print("                                                                    ")
    print("                                                                    ")
    print(colored("  +------------------------------------------------------------------------+","green"))
    print(colored("  |                             Find Lyrics                                |","white"))
    print(colored("  |------------------------------------------------------------------------|","green"))
    print(colored("  |Instructions.                                                           |","white"))
    print(colored("  |------------------------------------------------------------------------|","white"))
    print(colored("  |                             Menu Option 1                              |","white"))
    print(colored("  |------------------------------------------------------------------------|","white"))
    print(colored("  |Search song lyrics > Enter song name  |           Trees                 |","white"))
    print(colored("  |View > Use it's ID to get the lyrics  |           19751283              |","white"))
    print(colored("  |The song lyrics are automatically saved into the database               |","red"))
    print(colored("  |------------------------------------------------------------------------|","white"))
    print(colored("  |                             Menu Option 2                              |","white"))
    print(colored("  |------------------------------------------------------------------------|","white"))
    print(colored("  |Clear local database > Clear the saved lyrics from the local database   |","white"))
    print(colored("  |------------------------------------------------------------------------|","white"))
    print("                                                                    ")
    print("                                                                    ")
    menu() #here I call the menu function after the introductory message above.
