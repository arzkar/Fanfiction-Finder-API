from fastapi import FastAPI
from find import find_fic
import uvicorn

app = FastAPI()


@app.get("/")
def index():
    return {'API': 'Fanfiction Finder', 'Author': 'arzkar'}


@app.get("/search/")
def search():
    return {'Search Examples': [
        "['For ao3 works searching:','https://fanfictionapi.repl.co/search/ao3 Harry Potter and the Prince of Slytherin']",
        "['For ao3 series searching:','https://fanfictionapi.repl.co/search/ao3 Harry Potter and the Prince of Slytherin series']",
        "['For ffn story searching','https://fanfictionapi.repl.co/search/ffn cadmean victory']"
    ]}


@app.get("/search/{fic_name}")
def get_fic(fic_name: str):
    res = find_fic(fic_name)
    return res


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000)
