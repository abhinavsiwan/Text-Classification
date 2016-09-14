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

    # used during accuracy and recall calculation
    ham_file_count = 0
    spam_file_count = 0

    # No of files classified as ham or spam
    ham_classified_true = 0
    spam_classified_true = 0
    ham_classified_false = 0
    spam_classified_false = 0

    fout = open("nboutput.txt", "w")
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
                    fout.writelines("ham " + root[root.index("dev"):] + "/" + file + "\n")
                else:
                    ham_classified_false += 1
                    fout.writelines("spam " + root[root.index("dev"):] + "/" + file + "\n")
            elif "spam" in root:
                spam_file_count += 1
                if prob_spam_file > prob_ham_file:
                    spam_classified_true += 1
                    fout.writelines("spam " + root[root.index("dev"):] + "/" + file + "\n")
                else:
                    spam_classified_false += 1
                    fout.writelines("ham " + root[root.index("dev"):] + "/" + file + "\n")

    accuracy_ham = ham_classified_true/ham_file_count
    accuracy_spam = spam_classified_true/spam_file_count

    # calculating precision for ham and spam
    precision_spam = spam_classified_true/(spam_classified_true + ham_classified_false)
    precision_ham = ham_classified_true/(ham_classified_true + spam_classified_false)

    # calculating recall for ham and spam
    recall_spam = spam_classified_true/spam_file_count
    recall_ham = ham_classified_true/ham_file_count

    # calculating f1 score for ham and spam
    f1_spam = (2 * precision_spam * recall_spam)/(precision_spam + recall_spam)
    f1_ham = (2 * precision_ham * recall_ham)/(precision_ham + recall_ham)

    print("Total ham files:" + str(ham_file_count))
    print("Total spam files:" + str(spam_file_count))
    print("Total ham classified true:" + str(ham_classified_true))
    print("Total ham classified false:" + str(ham_classified_false))
    print("Total spam classified true:" + str(spam_classified_true))
    print("Total spam classified false:" + str(spam_classified_false))
    print()
    print("ham accuracy:" + str(accuracy_ham))
    print("spam accuracy:" + str(accuracy_spam))
    print()
    print("spam precision:" + str(precision_spam))
    print("spam recall:" + str(recall_spam))
    print("spam F1 Score:" + str(f1_spam))
    print()
    print("ham precision:" + str(precision_ham))
    print("ham recall:" + str(recall_ham))
    print("ham F1 Score:" + str(f1_ham))


if __name__ == "__main__":main()