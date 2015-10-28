#!/usr/bin/env python3
task = 'spell checker Without Dictionary' \
       'calculate detection accuracy'

from .preprocessing import utilities


def process_trigrams():
    import math
    from collections import Counter
    trigrams = utilities.get_trigrams(utilities.get_words_set())
    total_trigrams = len(trigrams)
    top_20_percent = trigrams.most_common(math.ceil(0.2 * total_trigrams))
    normalized_trigrams_ = Counter()
    for trigram in top_20_percent:
        normalized_trigrams_[trigram[0]] = trigram[1] / total_trigrams
    return normalized_trigrams_

normalized_trigrams = process_trigrams()


def calculate_score(word):
    index = 0
    score = 0
    while (index + 2) < len(word):
        score += normalized_trigrams[word[index:index + 3]]
        index += 1
    return score / len(word)


def get_scores():
    sentences = utilities.get_all_sentences()

    test_data = utilities.parse_sentences(sentences)

    sentences = utilities.sanitize_sentences(sentences)

    total_correct_words = 0
    total_incorrect_words = 0
    total_correct_words_score = 0
    total_incorrect_words_score = 0
    for sentence in sentences:
        words = sentence.split()
        for word in words:
            total_correct_words_score += calculate_score(word)
        total_correct_words += len(words)

    for incorrect_word in test_data:
        # test_data[incorrect_word] = corresponding correct word
        total_correct_words_score += calculate_score(test_data[incorrect_word])
        total_incorrect_words_score += calculate_score(incorrect_word)
        if len(incorrect_word) > 2:
            total_incorrect_words += 1
        if len(test_data[incorrect_word]) > 2:
            total_correct_words += 1
    average_correct_words_score = total_correct_words_score / total_correct_words
    average_incorrect_words_score = total_incorrect_words_score / total_incorrect_words
    # print(total_correct_words, total_correct_words_score, len(incorrect_words), total_incorrect_words_score)

    return [average_correct_words_score, average_incorrect_words_score]


def get_threshold(scores):
    return (scores[0] + scores[1]) / 2


def calculate_detection_accuracy(threshold, test_data):
    correctly_detected = 0
    for incorrect_word in test_data:
        if calculate_score(incorrect_word) < threshold:
            correctly_detected += 1
    accuracy = (correctly_detected/len(test_data)) * 100
    # print("Accuracy", accuracy, "%")
    return accuracy


def calculate_accuracies(test_data=None, runs=1):
    #  TODO(dt) if needed, implement calculation of correction accuracy percentage

    threshold = get_threshold(get_scores())
    detection_accuracy = 0

    for run in range(runs):
        print('Iteration', run)
        if test_data is None:
            test_data = utilities.parse_sentences(utilities.get_random_300_sentences())
        print(len(test_data), "tagged erroneous words found in randomly selected 300 sentences")

        detection_accuracy += calculate_detection_accuracy(threshold, test_data)
    # return {'detection_accuracy_percentage': detection_accuracy}
    return detection_accuracy/runs


def compare_trigram_with_dictionary():
    """
    compares detection accuracy of trigram approach with dictionary approach
    """
    from .preprocessing import utilities
    from . import task0
    from . import task1

    utilities.print_banner('Comparing Trigram approach against Dictionary approach')

    words_set = utilities.get_words_set()
    test_data = utilities.parse_sentences(utilities.get_random_300_sentences())

    utilities.print_banner("Dictionary approach")
    dict_approach = task0.calculate_detection_accuracy(words_set=words_set, test_data=test_data)
    print("Dictionary approach accuracy", dict_approach, "%")

    utilities.print_banner("Trigram approach")
    tri_approach = task1.calculate_accuracies(test_data=test_data)
    print("Trigram approach accuracy ", tri_approach, "%")

    utilities.print_banner("Comparison")
    print("Dictionary approach:", dict_approach, "% || Trigram approach", tri_approach, "%")

if __name__ == "__main__":
    print("Trigram approach accuracy", calculate_accuracies(), '%')
    compare_trigram_with_dictionary()
