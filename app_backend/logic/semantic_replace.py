import os
import re

from itertools import groupby

import gensim
from sklearn.metrics.pairwise import cosine_similarity


current_dir = os.path.dirname(os.path.realpath(__file__))
model = None


def _prepare_model(fast_model_path):

    model_path = os.path.join(current_dir, "models", "GoogleNews-vectors-negative300.bin")
    temp_model = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True)
    temp_model.init_sims(replace=True)
    
    temp_model.save(fast_model_path)


def _get_model():
    global model
    if model is None:
        fast_model_path = os.path.join(current_dir, "models", "GoogleNews-vectors-gensim-normed.bin")

        if not os.path.exists(fast_model_path):
            _prepare_model(fast_model_path)
        
        model = gensim.models.KeyedVectors.load(fast_model_path, mmap='r')

    return model


def _clean_input(phrase_or_sentence):
    all_words = re.findall(r'\b\w+\b', phrase_or_sentence)
    original_words = all_words
    cleaned_words = [word.lower() if word in model else None for word in all_words]
    return original_words, cleaned_words


def _split_to_sentences(text):
    """
    A simple implementation of text split to sentences.
    It does not take into account cases when "." can be used for something else, except end of a sentence.
    """
    return [s for s in [s.strip() for s in text.split('.')] if s]


def _slide_thru(words, window_size):
    """
    This function allows to go thru a set of words and get all the combinations of phrases (adjacent words).
    E.g. for "I love my cat" and window_size==2 the output will be:
    - I
    - I love
    - love
    - love my
    - my
    - my cat
    - cat
    """
    for start_index in range(0, len(words)):
        for window_len in range(window_size):
            end_index = start_index + window_len + 1
            if end_index <= len(words):
                yield words[start_index:end_index], start_index, end_index


def _find_all_replacements(text, standard_phrases):
    result = []
    model = _get_model()

    sentences = _split_to_sentences(text)

    clean_standard_phrase_words = [_clean_input(standard_phrase) for standard_phrase in standard_phrases]

    for sentence in sentences:
        suggestions = []
        sentence_result = {
            "sentence": sentence,
            "suggestions": suggestions,
        }

        original_sentence_words, cleaned_sentence_words = _clean_input(sentence)
        for original_std_phrase, clean_std_phrase in clean_standard_phrase_words:
            standard_phrase_embedding = sum([model[word] for word in clean_std_phrase if word])
            
            for window, window_start_index, window_end_index in _slide_thru(cleaned_sentence_words, 5):
                clean_window = [model[word] for word in window if word]
                if len(clean_window) == 0:
                    continue
                window_vector = sum(clean_window)

                similarity = cosine_similarity(
                    window_vector.reshape(1, -1),
                    standard_phrase_embedding.reshape(1, -1)
                )

                if similarity[0][0] > 0.10:  # add a minimum threshold that makes sense (IMO)
                    #print(window, original_std_phrase, similarity[0][0])
                    suggestions.append({
                        "original_phrase": " ".join(original_sentence_words[window_start_index:window_end_index]),
                        "replacement": " ".join([s.lower() for s in original_std_phrase]),
                        "similarity_score": round(float(similarity[0][0]), 3),
                    })

        result.append(sentence_result)
    
    return result


def _average_similary_per_replacement(all_suggestions):
    replacement_avg = {}
    key_replacement = lambda s: s["replacement"]
    for replacement, suggestions in groupby(sorted(all_suggestions, key=key_replacement), key_replacement):
        ls = list(suggestions)
        replacement_avg[replacement] = sum(s["similarity_score"] for s in ls) / len(ls)

    return replacement_avg



def _filter_sort(replacements, top, similarity_threshold):
    result = []
    for sentence_suggestion in replacements:
        all_suggestions = sentence_suggestion["suggestions"]

        # get average score by replacement so we can filter out suggestions below average
        replacement_avg = _average_similary_per_replacement(all_suggestions)

        key_original_phrase = lambda s: s["original_phrase"]
        key_similarity = lambda s: s["similarity_score"]
        
        grouped_by_original_phrase = {
            k: sorted(list(v), key=key_similarity, reverse=True)
            for k, v in groupby(sorted(all_suggestions, key=key_original_phrase), key_original_phrase)
        }
        
        good_suggestions = []
        for suggestions in grouped_by_original_phrase.values():
            for suggestion in suggestions[0:top]:
                if suggestion["similarity_score"] > replacement_avg[suggestion["replacement"]] and suggestion["similarity_score"] > similarity_threshold:
                    good_suggestions.append(suggestion)

        result.append({
            "sentence": sentence_suggestion["sentence"],
            "suggestions": good_suggestions,
        })

    return result



def find_replacements(text, standard_phrases, top=5, similarity_threshold=0.2):
    all_possible_replacements = _find_all_replacements(text, standard_phrases)
    return _filter_sort(all_possible_replacements, top, similarity_threshold)
