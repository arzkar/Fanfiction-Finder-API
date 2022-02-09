# Copyright 2021 Arbaaz Laskar

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from find import find_fic
import uvicorn

app = FastAPI(docs_url=None, redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


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
