from fastapi import FastAPI
from find import find_fic
import uvicorn

app = FastAPI()


@app.get("/")
def index():
    return {'API': 'Fanfiction Finder', 'Author': 'arzkar'}


@app.get("/search/{fic_name}")
def get_fic(fic_name: str):
    res = find_fic(fic_name)
    return res


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000)
