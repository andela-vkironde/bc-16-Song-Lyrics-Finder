from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

# Create a declarative_base base to be imported in every table created.

Base = declarative_base()


# Below:A lyrics store table to store the
# songs and their lyrics
class LyricsStore(Base):
    __tablename__ = 'lyric_store'

    # Columns for the table lyric_store
    id = Column(Integer, primary_key=True)
    song_id = Column(String(200), nullable=False)
    song_lyrics = Column(String(1062), nullable=False)

    def __init__(self, song_id, song_lyrics):
        self.song_id = song_id
        self.song_lyrics = song_lyrics


# Below, I create an engine to store data in the local lyrics.db file.
engine = create_engine('sqlite:///lyrics.db')

# Create all tables in the engine. 
Base.metadata.create_all(engine)
