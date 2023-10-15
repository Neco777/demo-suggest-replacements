import json
from app_backend.logic.semantic_replace import find_replacements, _slide_thru

def test_slide_thru():
    windows = [w for (w, _, _) in _slide_thru("I love my cat".split(), 2)]

    assert windows == [
        ["I"],
        ["I", "love"],
        ["love"],
        ["love", "my"],
        ["my"],
        ["my", "cat"],
        ["cat"],
    ]

def test_semantic_replace():
    task_sentences_input = """
        I love my cat
    """
    task_standard_phrases_input = [
        "tiny tiger",
        "big elephant",
    ]

    suggestions = find_replacements(task_sentences_input, task_standard_phrases_input, similarity_threshold=0.4)

    assert ["I love my cat"] == [s["sentence"] for s in suggestions]

    assert suggestions[0]["suggestions"] == [
        {
            "original_phrase": "cat",
            "replacement": "tiny tiger",
            "similarity_score": 0.497,
        },
        {
            "original_phrase": "my cat",
            "replacement": "tiny tiger",
            "similarity_score": 0.424,
        },
    ]


def test_semantic_replace_task_sample():
    task_sentences_input = """
        We should aim to be more efficient and look for ways to be more creative in our daily tasks.
    """
    task_standard_phrases_input = [
        "Optimal performance",
        "Utilize resources",   # need to replace the original Utilise
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
        "Exercise due diligence",
        "Maximize stakeholder value",
        "Prioritize tasks",    # need to replace the original Prioritise
        "Facilitate collaboration",
        "Monitor performance metrics",
        "Execute strategies",
        "Gauge effectiveness",
        "Champion change",
    ]

    suggestions = find_replacements(task_sentences_input, task_standard_phrases_input, similarity_threshold=0.4)

    assert suggestions == [
        {
            "sentence": "We should aim to be more efficient and look for ways to be more creative in our daily tasks",
            "suggestions": [
                {
                    "original_phrase": "and look for ways",
                    "replacement": "implement best practices",
                    "similarity_score": 0.428,
                },
                {
                    "original_phrase": "and look for ways to",
                    "replacement": "implement best practices",
                    "similarity_score": 0.428,
                },
                {
                    "original_phrase": "creative in our",
                    "replacement": "foster innovation",
                    "similarity_score": 0.401,
                },
                {
                    "original_phrase": "creative in our daily tasks",
                    "replacement": "prioritize tasks",
                    "similarity_score": 0.499,
                },
                {
                    'original_phrase': 'daily tasks',
                    'replacement': 'prioritize tasks',
                    'similarity_score': 0.654
                },
                {
                    'original_phrase': 'efficient and look for',
                    'replacement': 'implement best practices',
                    'similarity_score': 0.426
                },
                {
                    'original_phrase': 'efficient and look for',
                    'replacement': 'maintain a high standard',
                    'similarity_score': 0.402
                },
                {
                    'original_phrase': 'efficient and look for ways',
                    'replacement': 'implement best practices',
                    'similarity_score': 0.481
                },
                {
                    'original_phrase': 'efficient and look for ways',
                    'replacement': 'utilize resources',
                    'similarity_score': 0.415
                },
                {
                    'original_phrase': 'for ways',
                    'replacement': 'implement best practices',
                    'similarity_score': 0.412
                },
                {
                    'original_phrase': 'for ways to',
                    'replacement': 'implement best practices',
                    'similarity_score': 0.412
                },
                {
                    'original_phrase': 'in our daily tasks',
                    'replacement': 'prioritize tasks',
                    'similarity_score': 0.496
                },
                {
                    'original_phrase': 'look for ways',
                    'replacement': 'implement best practices',
                    'similarity_score': 0.428
                },
                {
                    'original_phrase': 'look for ways to',
                    'replacement': 'implement best practices',
                    'similarity_score': 0.428
                },
                {
                    'original_phrase': 'look for ways to be',
                    'replacement': 'implement best practices',
                    'similarity_score': 0.415
                },
                {
                    'original_phrase': 'our daily tasks',
                    'replacement': 'prioritize tasks',
                    'similarity_score': 0.601
                },
                {
                    'original_phrase': 'tasks',
                    'replacement': 'prioritize tasks',
                    'similarity_score': 0.82
                },
            ]
        },
    ]
