from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from typing import Optional, List
import requests
import os
from dotenv import load_dotenv
from pydantic import BaseModel, conint, constr

app = FastAPI(title="Movie Rating API")

load_dotenv()

Base = declarative_base()

class Movie(Base):
    __tablename__ = 'movies'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    imdb_id = Column(String(20), unique=True)
    title = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    genre = Column(String(255))
    director = Column(String(255))
    plot = Column(String(1024))
    poster = Column(String(512))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    ratings = relationship("Rating", back_populates="movie", cascade="all, delete-orphan")

class Rating(Base):
    __tablename__ = 'ratings'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"))
    name = Column(String(255), nullable=False)
    rate = Column(Float, nullable=False)
    description = Column(String(1024))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    movie = relationship("Movie", back_populates="ratings")

class Database:
    def __init__(self):
        self.engine = create_engine('sqlite:///movies.db', echo=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        
    def get_session(self):
        return self.Session()

class MovieAPI:
    def __init__(self):
        self.api_key = os.getenv('OMDB_API_KEY')
        self.base_url = "http://www.omdbapi.com/"
        
    def fetch_movie(self, title: str) -> Optional[dict]:
        params = {
            'apikey': self.api_key,
            't': title,
            'type': 'movie'
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            return data if data.get('Response') == 'True' else None
        except requests.RequestException as e:
            print(f"API Erro: {e}")
            return None

db = Database()
movie_api = MovieAPI()

class MovieBase(BaseModel):
    title: constr(max_length=255)
    year: conint(gt=1900, lt=datetime.now().year + 1)
    genre: constr(max_length=255)
    director: constr(max_length=255)

class MovieCreate(MovieBase):
    pass

class MovieUpdate(MovieBase):
    pass

class MovieResponse(MovieBase):
    id: int
    imdb_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class RatingBase(BaseModel):
    name: constr(max_length=255)
    rate: conint(ge=1, le=10)
    description: constr(max_length=1024)

class RatingCreate(RatingBase):
    movie_id: int

class RatingResponse(RatingBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

@app.post("/movies/", response_model=MovieResponse)
async def create_movie(movie: MovieCreate):
    with db.get_session() as session:
        api_data = movie_api.fetch_movie(movie.title)
        
        new_movie = Movie(
            title=movie.title,
            year=movie.year,
            genre=movie.genre,
            director=movie.director,
            imdb_id=api_data.get('imdbID') if api_data else None,
            plot=api_data.get('Plot') if api_data else None,
            poster=api_data.get('Poster') if api_data else None
        )
        
        session.add(new_movie)
        session.commit()
        session.refresh(new_movie)
        return new_movie

@app.put("/movies/{movie_id}", response_model=MovieResponse)
async def update_movie(movie_id: int, movie: MovieUpdate):
    with db.get_session() as session:
        db_movie = session.query(Movie).filter(Movie.id == movie_id).first()
        if not db_movie:
            raise HTTPException(status_code=404, detail="Filme não encontrado.")
            
        for key, value in movie.dict().items():
            setattr(db_movie, key, value)
            
        session.commit()
        session.refresh(db_movie)
        return db_movie

@app.post("/ratings/", response_model=RatingResponse)
async def create_rating(rating: RatingCreate):
    with db.get_session() as session:
        if not session.query(Movie).filter(Movie.id == rating.movie_id).first():
            raise HTTPException(status_code=404, detail="Filme não encontrado.")
            
        new_rating = Rating(**rating.dict())
        session.add(new_rating)
        session.commit()
        session.refresh(new_rating)
        return new_rating

@app.get("/movies/{movie_id}/ratings", response_model=List[RatingResponse])
async def get_movie_ratings(movie_id: int):
    with db.get_session() as session:
        ratings = session.query(Rating).filter(Rating.movie_id == movie_id).all()
        if not ratings:
            raise HTTPException(status_code=404, detail="Sem avaliações para este filme.")
        return ratings

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)