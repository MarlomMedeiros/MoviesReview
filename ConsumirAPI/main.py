from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os
import requests
import time
from typing import Optional, List, Dict
from dotenv import load_dotenv

Base = declarative_base()

class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    imdb_id = Column(String(20))
    title = Column(String(255))
    year = Column(Integer)
    genre = Column(String(255))
    director = Column(String(255))
    plot = Column(String(1024))
    poster = Column(String(512))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Database:
    def __init__(self):
        self.engine = create_engine('sqlite:///../movies.db')
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def get_session(self):
        return self.Session()

class OMDBClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('OMDB_API_KEY')
        self.base_url = "http://www.omdbapi.com/"
        self.db = Database()
    
    def search_movies(self, search_term: str) -> List[Dict]:
        params = {
            'apikey': self.api_key,
            's': search_term,
            'type': 'movie'
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('Search', []) if data.get('Response') == 'True' else []
        except requests.RequestException as e:
            print(f"Erro: {e}")
            return []

    def get_movie_details(self, imdb_id: str) -> Optional[Dict]:
        params = {
            'apikey': self.api_key,
            'i': imdb_id,
            'plot': 'full'
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            return data if data.get('Response') == 'True' else None
        except requests.RequestException as e:
            print(f"Erro: {e}")
            return None

    def sync_movies_to_db(self, search_term: str):
        movies = self.search_movies(search_term)
        
        with self.db.get_session() as session:
            for movie in movies:
                time.sleep(1)
                details = self.get_movie_details(movie['imdbID'])
                
                if not details:
                    continue
                    
                try:
                    year = int(details['Year'][:4])
                except ValueError:
                    continue
                
                movie_entry = Movie(
                    imdb_id=details['imdbID'],
                    title=details['Title'],
                    year=year,
                    genre=details['Genre'],
                    director=details['Director'],
                    plot=details['Plot'],
                    poster=details['Poster']
                )
                
                existing = session.query(Movie).filter_by(imdb_id=details['imdbID']).first()
                if existing:
                    for key, value in movie_entry.__dict__.items():
                        if key != '_sa_instance_state':
                            setattr(existing, key, value)
                else:
                    session.add(movie_entry)
                
                try:
                    session.commit()
                    print(f"Sincronizado: {details['Title']}")
                except Exception as e:
                    session.rollback()
                    print(f"Erro ao sicronizar:: {details['Title']}: {e}")

def main():
    client = OMDBClient()
    search_terms = ["Batman", "Superman", "Spider-Man"]
    
    for term in search_terms:
        print(f"\nSicronizando os filmes da franquia: {term}")
        client.sync_movies_to_db(term)

if __name__ == "__main__":
    main()