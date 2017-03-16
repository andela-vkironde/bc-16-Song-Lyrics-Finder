import json
import requests
import sys
import cmd

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from docopt import docopt, DocoptExit 
from prettytable import PrettyTable #Create my display table
from colorama import init, Back
init() 
from pyfiglet import Figlet
from termcolor import colored  #Print my welcoming instruction in colour
from tabulate import tabulate #not used yet

from dbmodel import LyricsStore,Base


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
    if len(track_id)<4:
        print("Enter the whole track id.")
    # else:
    #     #search local database

    else:
        api_key = "fede23bab51e23e61888932cd118ca2c"
        response = requests.get("https://api.musixmatch.com/ws/1.1/track.lyrics.get?track_id="+track_id+"&apikey="+api_key)
    
        output = json.loads(response.text)
        body = len(output["message"]["body"])
        if body == 0:
            print("No lyrics found")

        else:
            print(output["message"]["body"]["lyrics"]["lyrics_body"])
           # print(output['message']['body']['lyrics']['lyrics_body'])

           #Function to save the lyrics
            def save_lyrics(track_id):
                """save <song_id> - store song details and lyrics locally"""
                try:
                    song_id = track_id
                    song_lyrics = output
                    #If the song has no lyrics
                    if body == 0:
                        print("Please try another track_id. This one has no lyrics.")
                
                    else:#Store lyrics found on lyrics db
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
                                response = requests.get("http://api.musixmatch.com/ws/1.1/track.search")
                                try:  #This decodes the JSON
                                    response_data = response.json()
                                    body = response_data['message']['body']['track_list']
                                    All_songs = []
                                    track_table = PrettyTable(['Track ID', 'Song Name', 'Artist Name'])
                                    for result in body:
                                        song_details = []
                                        result_id = result['track']['track_id']
                                        title = result['track']['track_name']
                                        artist_name = result['track']['artist_name']
                                        song_details.insert(0, result_id)
                                        song_details.insert(1, title)
                                        song_details.insert(2, artist_name)
                                        track_table.add_row([result_id, title, artist_name])
                                        All_songs.append(song_details)
                    
                                        print(track_table)
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
    """
    song menu - Seeks user choice
    """
    print(colored(Figlet(font='straight').renderText('\t[1] Search for a song.'),"white"))
    print(colored(Figlet(font='straight').renderText('\t[2] Clear local song database.'),"white"))
    print(colored(Figlet(font='straight').renderText('\t[q] Quit.'),"white"))

    choice=input(colored(Figlet(font="straight").renderText('\tI want to..?'),"white"))

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
                    
                    print(track_table)
            except json.decoder.JSONDecodeError:
                print("Cannot Decode JSON")

        search_song()
        view_lyrics()
                
    elif choice == "2":
        clear_lyricstore()
    elif choice == "q":
        print(colored(Figlet(font='straight').renderText('\t I thought you were serious about this man! Bye.'),"white"))
        quit()
        
    else:
        print(colored(Figlet(font='straight').renderText('\t Comeon!Thats not in the choices'),"white"))
        print(colored(Figlet(font='straight').renderText('\t Lets try that again.'),"white"))
        menu()

#Brighten up my interface using termcolor
class LyricsStore (cmd.Cmd):
    print(colored(".-." * 20,"white"))
    print(colored(Figlet(font='slant').renderText('\t      K A R A B L E'),"white"))
    print(colored(".-." * 20,"white"))
    print(colored("\t\t\t     The Karaoke Bible. ","white"))
    print(colored(" \t           To use at every singing opportunity.","white"))
    print("                                                                    ")
    print(colored(" \t                        Seriously.","white"))
    print("                                                                    ")
    print("                                                                    ")
    print(colored(Figlet(font='slant').renderText('\t      lets do this'),"white"))
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
