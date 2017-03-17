![The App](https://cdn-images-1.medium.com/max/800/1*TiJXsrlqhbgkV5J8C-qajA.png)


##The Task:

For this project, you will be expected to make use of MusixMatch API or RapGenius API.

As a user, I can perform the following operations:

song find `<search_query_string>` - Returns a list of songs that match the criteria.

song view `<song_id>` - View song lyrics based on it’s id. Should be optimized by checking if there’s a local copy before checking online.

song save `<song_id>` - Store song details and lyrics locally.

song clear - Clear entire local song database.


##GETTING STARTED:

 - Navigate to a directory of choice 
 
 - git clone https://github.com/Mnickii/bc-16-Song-Lyrics-Finder.git 
 
 - `cd bc-16-song-lyrics-finder`

 - Activate Virtual Environment
 
 - pip insall -r requirements.txt
 -
 - run dbmodel.py on command line, on the chosen directory, to create local database in same directory
 
 - run python lyric.py on command line
 -
 
## Functionalities:##
`Enter the song name` - returns the top 10 artists based on song_name and returns Track ID, Song Name and Artist Name(s) on a table. Pretty Table module is used for this and term color is used for the display color. The Track ID will be used to find lyrics.

Usage:

`Enter the song name` Trees should display top 10 performances with the title Trees.

`Enter the track ID from above results` - Displays the Lyrics based on Track ID entered.

Usage:

`Enter Track ID` 19751283 display lyrics,  from the Track IDs generated from find Trees. Trees, in this case, is a song by Twenty One Pilots, whose Track ID is 19751283.

 In this application, the song lyrics are automatically saved into the database after every successful search.

    Clear the entire local database.

Usage :

Choosing to clear the database will clear entire local database.

    Quit

Usage:

Quits from the interactive session.
