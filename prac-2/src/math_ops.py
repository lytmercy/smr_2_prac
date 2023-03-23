import math
import numpy as np


def coef_adaptability(phrase_bigrams, statistics_bigrams):
    """Function for calculating coefficient of adaptability"""
    # Set value from statistics_bigrams dictionary to phrase_bigrams dictionary,
    # if key in phrase_bigrams dict same as key in statistics_bigrams dict.
    for phrase_bigram_key in phrase_bigrams:
        if phrase_bigram_key in statistics_bigrams:
            if statistics_bigrams[phrase_bigram_key] == 0:
                phrase_bigrams[phrase_bigram_key] = 1
            else:
                phrase_bigrams[phrase_bigram_key] = statistics_bigrams[phrase_bigram_key]

    # Calculate meaning of phrase fit
    num_phrase_bigrams = len(phrase_bigrams)
    phrase_bigrams_array = np.array(list(phrase_bigrams.values()), dtype=np.int64)
    return np.power(np.prod(phrase_bigrams_array, dtype=np.complex_), 1/num_phrase_bigrams)


def threshold_r(s_phrases, p_phrases):
    """"""
    min_s_phrase = np.min(s_phrases)
    max_p_phrase = np.max(p_phrases)

    return (min_s_phrase + max_p_phrase) / 2
