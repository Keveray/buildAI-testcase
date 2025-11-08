import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
import uvicorn
from models import Base
from database import engine 
from routers import cars_router, users_router, incidents_router 

app = FastAPI(title="UCAR-TODOR Simple API")

app.include_router(users_router) 
app.include_router(cars_router)
app.include_router(incidents_router) 

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "create_tables":
        create_tables()
        print("Tables created")
    else:
        uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)