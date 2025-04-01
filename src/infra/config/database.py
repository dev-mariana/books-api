from sqlmodel import create_engine
from .environment import DB_URL

engine = create_engine(DB_URL)
