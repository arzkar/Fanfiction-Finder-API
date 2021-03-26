from fastapi import FastAPI
from find import find_fic
import uvicorn

app = FastAPI()


@app.get("/")
def index():
    return {
        'API': 'Fanfiction Finder',
        'Author': 'arzkar',
        'Search Examples': [
            "['For ao3 works searching:','https://fanfictionapi.repl.co/search?q=ao3 Harry Potter and the Prince of Slytherin']",
            "['For ao3 series searching:','https://fanfictionapi.repl.co/search?q=ao3 Harry Potter and the Prince of Slytherin series']",
            "['For ffn story searching','https://fanfictionapi.repl.co/search?q=ffn cadmean victory']",
            "['To search using url','https://fanfictionapi.repl.co/search?q=https://www.fanfiction.net/s/11446957/1/A-Cadmean-Victory']"
        ]

    }


@app.get("/search")
def get_fic(q: str):
    res = find_fic(q)
    return res


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000)
