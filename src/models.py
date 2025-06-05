from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from eralchemy2 import render_er

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  
db = SQLAlchemy(app)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(40), nullable=False)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    created: Mapped[datetime] = mapped_column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    favorites = db.relationship('Favorite', backref='user', lazy=True)

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    diameter: Mapped[str] = mapped_column(String(100), nullable=False)
    rotation_period: Mapped[str] = mapped_column(String(100), nullable=False)
    orbital_period: Mapped[str] = mapped_column(String(100), nullable=False)
    gravity: Mapped[str] = mapped_column(String(100), nullable=False)
    population: Mapped[str] = mapped_column(String(100), nullable=False)
    climate: Mapped[str] = mapped_column(String(100), nullable=False)
    terrain: Mapped[str] = mapped_column(String(100), nullable=False)
    surface_water: Mapped[str] = mapped_column(String(100), nullable=False)
    created: Mapped[datetime] = mapped_column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    edited: Mapped[datetime] = mapped_column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    favorites = db.relationship('Favorite', backref='planet', lazy=True)

class Vehicle(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    vehicle_class: Mapped[str] = mapped_column(String(100), nullable=False)
    manufacturer: Mapped[str] = mapped_column(String(100), nullable=False)
    length: Mapped[str] = mapped_column(String(100), nullable=False)
    cost_in_credits: Mapped[str] = mapped_column(String(100), nullable=False)
    crew: Mapped[str] = mapped_column(String(100), nullable=False)
    max_atmosphering_speed: Mapped[str] = mapped_column(String(100), nullable=False)
    cargo_capacity: Mapped[str] = mapped_column(String(100), nullable=False)
    consumables: Mapped[str] = mapped_column(String(100), nullable=False)
    url: Mapped[str] = mapped_column(String(200), nullable=False)
    created: Mapped[datetime] = mapped_column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    edited: Mapped[datetime] = mapped_column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    favorites = db.relationship('Favorite', backref='vehicle', lazy=True)

class People(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    birth_year: Mapped[str] = mapped_column(String(100), nullable=False)
    eye_color: Mapped[str] = mapped_column(String(100), nullable=False)
    gender: Mapped[str] = mapped_column(String(100), nullable=False)
    hair_color: Mapped[str] = mapped_column(String(100), nullable=False)
    height: Mapped[str] = mapped_column(String(20), nullable=False)
    mass: Mapped[str] = mapped_column(String(40), nullable=False)
    skin_color: Mapped[str] = mapped_column(String(20), nullable=False)
    homeworld: Mapped[str] = mapped_column(String(40), nullable=False)
    url: Mapped[str] = mapped_column(String(100), nullable=False)
    created: Mapped[datetime] = mapped_column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    edited: Mapped[datetime] = mapped_column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    favorites = db.relationship('Favorite', backref='people', lazy=True)

class Favorite(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey('user.id'), nullable=False)
    people_id: Mapped[int] = mapped_column(db.ForeignKey('people.id'), nullable=True)
    vehicle_id: Mapped[int] = mapped_column(db.ForeignKey('vehicle.id'), nullable=True)
    planet_id: Mapped[int] = mapped_column(db.ForeignKey('planet.id'), nullable=True)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'people_id', 'vehicle_id', 'planet_id', name='_user_fav_uc'),)



    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }