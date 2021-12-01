# from database import  engine
from routers import post, user, auth, vote
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 


# Setting up Dependency for models
# models.Base.metadata.create_all(bind=engine)
# No need to create tables, since we are using Alembic

# Create app
app = FastAPI()

# Setup CORS 
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/') 
def read_root():
    return {"Message": "Hello, Welcome to fastapi world!!"} 

        