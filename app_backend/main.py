from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from logic.semantic_replace import find_replacements

app = FastAPI()

print('started!')

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello!"}


default_sentences = """
    In today's meeting, we discussed a variety of issues affecting our department.
    The weather was unusually sunny, a pleasant backdrop to our serious discussions.
    We came to the consensus that we need to do better in terms of performance.
    Sally brought doughnuts, which lightened the mood.
    It's important to make good use of what we have at our disposal.
    During the coffee break, we talked about the upcoming company picnic.
    We should aim to be more efficient and look for ways to be more creative in our daily tasks.
"""
default_standard_phrases = [
    "Optimal performance",
    "Utilize resources",
    "Enhance productivity",
    "Conduct an analysis",
    "Maintain a high standard",
    "Implement best practices",
    "Ensure compliance",
    "Streamline operations",
    "Foster innovation",
    "Drive growth",
    "Leverage synergies",
    "Demonstrate leadership",
]


@app.get("/api/try-suggest")
async def try_suggest(sentence = default_sentences, standard_phrases = default_standard_phrases):
    return find_replacements(sentence, standard_phrases, similarity_threshold=0.4)

from typing import List
from pydantic import BaseModel

class SuggestRequest(BaseModel):
    sentence: str
    standard_phrases: List[str]

@app.post("/api/try-suggest")
async def try_suggest(suggestRequest: SuggestRequest):
    return find_replacements(
        suggestRequest.sentence,
        suggestRequest.standard_phrases,
        similarity_threshold=0.4,
    )
