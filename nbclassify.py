import os
import sys
from os import listdir
from os.path import isfile, join
import json
from pprint import pprint
import math


def main():
    arg = sys.argv
    # directory = arg[1]
    directory = "../Spam or Ham/dev/"

    # read the json data from nbmodel.txt
    with open("nbmodel.txt") as data_file:
        data = json.load(data_file)

    # pprint(data["word_dict"])
    # pprint(data["word_dict"]["Subject:"])
    # print(data["vocab_size"])
    # print(data["spam_fcount"])
    # print(data["ham_fcount"])
    # print(data["spam_wcount"])
    # print(data["ham_wcount"])

    # calculate some data to be used in Naive Baye's calculation
    probab_spam = data["spam_wcount"]/data["vocab_size"]
    probab_ham = data["ham_wcount"]/data["vocab_size"]

    # used during accuracy calculation
    ham_file_count = 0
    spam_file_count = 0

    # files classified as ham or spam
    ham_classified_true = 0
    spam_classified_true = 0

    for root, subdir, subfiles in os.walk(directory):
        # print(root)
        files = [f for f in listdir(root) if isfile(join(root, f))]
        for file in files:
            # print(root + "/" + file)
            f = open(root + "/" + file, "r", encoding="latin1")
            words = f.read().strip().split()
            probab_spam_words = 0
            probab_ham_words = 0
            for w in words:
                # Added one smoothing
                if w in data["word_dict"]:
                    probab_ham_words += math.log((data["word_dict"][w]["ham_count"] + 1)/(data["ham_wcount"] +
                                                                                          data["vocab_size"]))
                    probab_spam_words += math.log((data["word_dict"][w]["spam_count"] + 1)/(data["spam_wcount"] +
                                                                                            data["vocab_size"]))

            prob_ham_file = math.log(probab_ham) + probab_ham_words
            prob_spam_file = math.log(probab_spam) + probab_spam_words
            if "ham" in root:
                ham_file_count += 1
                if prob_ham_file > prob_spam_file:
                    ham_classified_true += 1
            elif "spam" in root:
                spam_file_count += 1
                if prob_spam_file > prob_ham_file:
                    spam_classified_true += 1

    accuracy_ham = ham_classified_true/ham_file_count
    accuracy_spam = spam_classified_true/spam_file_count

    print("Total ham files:" + str(ham_file_count))
    print("Total spam files:" + str(spam_file_count))
    print("Total ham classified:" + str(ham_classified_true))
    print("Total spam classified:" + str(spam_classified_true))
    print("ham accuracy" + str(accuracy_ham))
    print("spam accuracy" + str(accuracy_spam))


if __name__ == "__main__":main()