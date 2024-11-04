from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.routers import scores, auth, users

app = FastAPI(root_path='/api', contact={'telegram': 'https://t.me/oshinogj'})

app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(scores.router)
app.include_router(auth.router)
app.include_router(users.router)


@app.get('/', tags=['Индекс'], summary='Попасть в начало API')
async def root():
    return {"message": "...100%"}
