import numpy as np
import json
# Importing libraries for text preprocessing
import re
import string
# Importing help functions for math operations in project
from math_ops import coef_adaptability, threshold_r


def clean_text(text):
    """
    Help function for cleaning text;
    :param text :type string: text for cleaning;
    :return: string text after cleaning.
    """
    # Make cleaning
    text = text.lower()
    text = re.sub(r"\d", '', text)
    text = re.sub(r"[%s]" % re.escape(string.punctuation), ' ', text)  # remove punctuations
    text = re.sub(r"\n", ' ', text)
    text = re.sub(r"\s+", ' ', text)

    return text


def calculate_bigrams(string_line):
    """
    Help function for calculating bigrams in string_line;
    :param string_line: text data;
    :return: dictionary with all bigrams and their entry statistics.
    """
    # Define dictionary of bigrams
    bigrams_dict = {}
    # Cleaning string
    clean_string = clean_text(string_line)
    # Calculate bigrams
    # # Iterate through the string with a step of 2 characters
    for i in range(0, len(clean_string), 1):
        if clean_string[i:i + 2] in bigrams_dict:
            # Adding one to the quantity of characters of the current pair to the statistics dictionary
            bigrams_dict[clean_string[i:i + 2]] += 1
        else:
            # Add the current pair of characters to the statistics dictionary
            bigrams_dict[clean_string[i:i + 2]] = 1

    return bigrams_dict


def calculate_training_statistics(file_path):
    """
    Help function for calculating statistics of first file for training statistics;
    :param file_path: string of path to file with training text;
    :return: dictionary with training statistics of bi-grams.
    """
    # Calculate statistics
    with open(file_path, 'r', encoding="utf-8") as file:
        # Read all lines from file
        string_data = file.read()
        # Define dictionary of statistics from calculating bigrams
        statistics_dict = calculate_bigrams(string_data)

    return statistics_dict


def calculate_inference_statistics(file_path, train_statistics):
    """
    Help function for calculating statistics of second and third file of adequate and inadequate text;
    :param file_path: string of path to file with text;
    :param train_statistics: dictionary with training statistics of bi-grams;
    :return: array with coefficient of adaptability for each line from file with text.
    """
    # Calculate statistics
    with open(file_path, 'r', encoding="utf-8") as file:
        # Read data per line from file to list of lines
        lines_data = file.readlines()
        # Define new list of coefficient of adaptability per line
        coef_per_line = np.array([])
        # Calculate coefficient of adaptability for all lines
        for line in lines_data:
            line_bigrams = calculate_bigrams(line)
            line_coef = coef_adaptability(line_bigrams, train_statistics)
            coef_per_line = np.append(coef_per_line, line_coef)

    return coef_per_line


def calculate_r_threshold(train_statistics):
    """
    Help function for calculating value of R threshold;
    :param train_statistics: dictionary with training statistics of bi-grams;
    :return: integer value of R threshold.
    """
    # Calculate coefficient of adaptability for correct phrases
    correct_s_phrases = calculate_inference_statistics("input/second_file_correct.txt", train_statistics)
    # Calculate coefficient of adaptability for incorrect phrases
    incorrect_p_phrases = calculate_inference_statistics("input/third_file_incorrect.txt", train_statistics)

    # Calculate R threshold for those statistics
    r_threshold = threshold_r(correct_s_phrases, incorrect_p_phrases)

    return int(r_threshold)


def calculate_q_coef_adaptability(train_statistics, line_text):
    """
    Help function for calculating Q coefficient of adaptability for input text from user;
    :param train_statistics: dictionary with training statistics of bigrams;
    :param line_text: string data of input text from user;
    :return:
    """
    # Calculate bigrams for input text
    line_bigrams = calculate_bigrams(line_text)
    # Calculate Q coefficient of adaptability for input text from user
    q_coef = coef_adaptability(line_bigrams, train_statistics)

    return int(q_coef)


def save_r_threshold(r_threshold, file_path):
    """
    Function for saving value of R threshold to txt file;
    :param r_threshold: value of R threshold in integer type;
    :param file_path: string of path to file;
    """
    with open(file_path, 'w') as file:
        file.write(str(r_threshold))


def read_r_threshold(file_path):
    """
    Function for read value of R threshold from txt file;
    :param file_path: string of path to file;
    :return: integer value of R threshold.
    """
    # Reading value from file
    with open(file_path, 'r') as file:
        r_threshold = int(file.read())

    return r_threshold


def save_statistics(statistics, file_path):
    """
    Function for saving dictionary of bigrams statistics for training text to json file;
    :param statistics: dictionary with training statistics of bigrams;
    :param file_path: string of path to file;
    """
    with open(file_path, 'w') as file:
        # Use the json.dump() function to write the dictionary to the file
        json.dump(statistics, file)


def read_statistics(file_path):
    """
    Function for read value of training statistics of bigrams from json file to dictionary;
    :param file_path: string of path to file;
    :return: dictionary with training statistics of bigrams.
    """
    with open(file_path, 'r') as file:
        # Use the json.load() function to read the dictionary from the file
        statistics = json.load(file)

    return statistics
