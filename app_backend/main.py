from fastapi import FastAPI
print(dir())
from logic.semantic_replace import find_replacements

app = FastAPI()

print('started!');

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


@app.get("/try-suggest")
async def try_suggest(sentence = default_sentences, standard_phrases = default_standard_phrases):
    return find_replacements(sentence, standard_phrases, similarity_threshold=0.4)
