import json
import requests
import sys
import cmd
import socket

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from prettytable import PrettyTable #Create my display table
from colorama import init #use in my display table
init() 
from pyfiglet import Figlet
from termcolor import colored  #Print my welcoming instruction in colour
from tabulate import tabulate #not used yet

from dbmodel import LyricsStore,Base  #import my database


#Start the session
mysession = sessionmaker()


engine = create_engine('sqlite:///lyrics.db')
# Bind the engine to the metadata of the Base class 


mysession.configure(bind=engine)

session = mysession()

#Function to view my lyrics
def view_lyrics():
    """view <song_id> - View song lyrics based on its ID. Optimized to check for local copy first."""
    track_id = input(colored("Enter the Track ID from the above results or q to quit: ","yellow"))
    if track_id == "q":
        quit()
    if len(track_id)<4:
        print(colored("Enter the whole track id.","yellow"))
        view_lyrics()
    else:
        # lyrics = session.query(LyricsStore).filter_by(song_id = str(track_id)).all() -not working. To fix.
        # print(lyrics["message"]["body"]["lyrics"]["lyrics_body"])
        api_key = "fede23bab51e23e61888932cd118ca2c"  
        response = requests.get("https://api.musixmatch.com/ws/1.1/track.lyrics.get?track_id="+track_id+"&apikey="+api_key)
    
        output = json.loads(response.text)
        body = len(output["message"]["body"])
        if body == 0:
            print(colored("No lyrics found","red"))
            print("Enter another Track ID.")
            view_lyrics()

        else:
            print(colored(output["message"]["body"]["lyrics"]["lyrics_body"],"yellow"))
           
            def save_lyrics(track_id):
                """save <song_id> - store song details and lyrics locally"""
                try:
                    song_id = track_id
                    song_lyrics = output
                    #If the song has no lyrics
                    if body == 0:
                        print(colored("Please try another track_id. This one has no lyrics.","yellow"))
                
                    else:#Store lyrics found on lyrics db
                        lyrics_found = LyricsStore(song_id, json.dumps(song_lyrics))
                        session.add(lyrics_found)
                        session.commit()
                        print(colored(Figlet(font='slant').renderText('\t      Lyrics saved!'),"yellow"))
                        print("                                                                      ")
                        print("                                                                      ")
                        print(colored(Figlet(font='slant').renderText('\t      That was fun :)'),"yellow"))
                        choice2 = input(colored("Print N to exit and M to go to menu.","yellow"))
                        #Go back to menu
                        if choice2=="M":
                            def menu():
                                """
                                song menu - Seeks user choice
                                """
                                print(colored(Figlet(font='straight').renderText('\t[1] Search song.'),"yellow"))
                                print(colored(Figlet(font='straight').renderText('\t[2] Clear local database.'),"yellow"))
                                print(colored(Figlet(font='straight').renderText('\t[q] Quit.'),"yellow"))

                                choice=input(colored(Figlet(font="straight").renderText('\tI want to..?')))
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
                                            body = response_data['message']['body']['track_list']
                                            list_of_all_songs = []
                                            track_table = PrettyTable(['Track ID', 'Song Name', 'Artist Name'])
                                            for result in body:
                                                song_details = []
                                                result_id = result['track']['track_id']
                                                title = result['track']['track_name']
                                                artist_name = result['track']['artist_name']
                                                song_details.insert(0, result_id)
                                                song_details.insert(1, title)
                                                song_details.insert(2, artist_name)
                                                track_table.add_row(
                                                                 [result_id, title, artist_name])
                                                list_of_all_songs.append(song_details)
                                            else:
                                                print(track_table)
                                        except json.decoder.JSONDecodeError:
                                            print("Cannot Decode JSON")

                                    search_song()
                                    view_lyrics()
                
                                elif choice == "2":
                                    clear_lyricstore()
                                elif choice == "q":
                                    print(colored(Figlet(font='straight').renderText('\t I thought you were serious about this man! Bye.'),"yellow"))
                                    quit()
                                else:
                                    print(colored(Figlet(font='straight').renderText('\t Comeon!Thats not in the choices'),"yellow"))
                                    print(colored(Figlet(font='straight').renderText('\t Lets try that again.'),"yellow"))
                            menu()

                        else: #Stop the song search and print goodbye
                            print(colored(Figlet(font='slant').renderText('\t      Goodbye :)'),"yellow"))

                except socket.timeout:       
                    print(colored("Timeout raised and caught","red"))

            save_lyrics(track_id)

def clear_lyricstore():
    """ song clear - Clear entire local song database."""

    choice1=input(colored("Are you sure about this? Enter Y/N","red"))
    if choice1 == "Y":
        Base.metadata.drop_all(bind=engine)
        print(colored("Database cleared successfully.","yellow"))
        Base.metadata.create_all(bind=engine)
    else:
        print(colored(Figlet(font='slant').renderText('\t      Good Choice!'),"yellow"))
        session.rollback() # Drop all tables then recreate them
       #Engage the user in choice
def menu():
    """
    song menu - Seeks user choice
    """
    print(colored(Figlet(font='straight').renderText('\t[1] Search song.'),"yellow"))
    print(colored(Figlet(font='straight').renderText('\t[2] Clear local database.'),"yellow"))
    print(colored(Figlet(font='straight').renderText('\t[q] Quit.'),"yellow"))

    choice=input(colored(Figlet(font="straight").renderText('\tI want to..?')))

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
                body = response_data['message']['body']['track_list']
                list_of_all_songs = []
                track_table = PrettyTable(['Track ID', 'Song Name', 'Artist Name'])
                for result in body:
                    song_details = []
                    result_id = result['track']['track_id']
                    title = result['track']['track_name']
                    artist_name = result['track']['artist_name']
                    song_details.insert(0, result_id)
                    song_details.insert(1, title)
                    song_details.insert(2, artist_name)
                    track_table.add_row(
                                    [result_id, title, artist_name])
                    list_of_all_songs.append(song_details)
                else:
                    print(track_table)
            except json.decoder.JSONDecodeError:
                print("Cannot Decode JSON")

        search_song()
        view_lyrics()
                
    elif choice == "2":
        clear_lyricstore()
    elif choice == "q":
        print(colored(Figlet(font='straight').renderText('\t I thought you were serious about this man! Bye.'),"yellow"))
        quit()
        
    else:
        print(colored(Figlet(font='straight').renderText('\t Comeon!Thats not in the choices'),"yellow"))
        print(colored(Figlet(font='straight').renderText('\t Lets try that again.'),"yellow"))
        menu()

#Brighten up my interface using termcolor and pyfiglet
class LyricsStore (cmd.Cmd):
    print(colored(".-." * 25,"yellow"))
    print(colored(Figlet(font='slant').renderText('\t      K A R A B L E'),"yellow"))
    print(colored(".-." * 25,"yellow"))
    print(colored("\t\t\t     The Karaoke Bible. ","yellow"))
    print(colored(" \t           To use at every singing opportunity.","yellow"))
    print("                                                                    ")
    print(colored(" \t                        Seriously.","yellow"))
    print(colored(Figlet(font='slant').renderText('\t      lets do this'),"yellow"))
    print(colored("  |------------------------------------------------------------------------|","yellow"))
    print(colored("  |                             Menu Option 1                              |","yellow"))
    print(colored("  |------------------------------------------------------------------------|","yellow"))
    print(colored("  |Search song lyrics > Enter song name  |           Trees                 |","yellow"))
    print(colored("  |View > Use it's ID to get the lyrics  |           19751283              |","yellow"))
    print(colored("  |The song lyrics are automatically saved into the database               |","red"))
    print(colored("  |------------------------------------------------------------------------|","yellow"))
    print(colored("  |                             Menu Option 2                              |","yellow"))
    print(colored("  |------------------------------------------------------------------------|","yellow"))
    print(colored("  |Clear local database > Clear the saved lyrics from the local database   |","yellow"))
    print(colored("  |------------------------------------------------------------------------|","yellow"))
    print("                                                                    ")
    print("                                                                    ")
    menu() #here I call the menu function after the introductory message above.
