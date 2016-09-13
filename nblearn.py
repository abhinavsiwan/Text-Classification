import sys
import os
from os import listdir
from os.path import isfile, join
import json

# spam_dict = dict()
# ham_dict = dict()
word_dict = dict()


class Model():
    # serialize the data and store it in a file nbmodal.txt. This file will be used as input to nbclassify.py
    def __init__(self, vocab_size, spam_fcount, ham_fcount, spam_wcount, ham_wcount, word_dict=None):
        self.vocab_size = vocab_size
        self.spam_fcount = spam_fcount
        self.ham_fcount = ham_fcount
        self.spam_wcount = spam_wcount
        self.ham_wcount = ham_wcount
        self.word_dict = word_dict


def main():
    arg = sys.argv
    # directory = arg[1]
    directory = "../Spam or Ham/train/"

    wordcount_spam = 0     # No of words in spam
    wordcount_ham = 0      # No of words in ham
    spam_file_count = 0    # No of files in spam
    ham_file_count = 0     # No of file in ham

    # print(directory)
    punctuation_list = [',', '.', ':', '_', '-', '|', ';']
    for root, subdir, subfiles in os.walk(directory):
        # print(root)
        if "ham" in root:
            files = [f for f in listdir(root) if isfile(join(root, f))]
            for file in files:
                ham_file_count += 1
                # print(root + "/" + file)
                f = open(root + "/" + file, "r", encoding="latin1")
                words = f.read().strip().split()
                for w in words:
                    if w in word_dict:
                        word_dict[w]['ham_count'] += 1
                    else:
                        word_dict[w] = {"spam_count": 0, "ham_count": 1}
                    wordcount_ham += 1
        elif "spam" in root:
            files = [f for f in listdir(root) if isfile(join(root, f))]
            for file in files:
                spam_file_count += 1
                # print(root + " " + file)
                f = open(root + "/" + file, "r", encoding="latin1")
                words = f.read().strip().split()
                for w in words:
                    if w in word_dict:
                        word_dict[w]['spam_count'] += 1
                    else:
                        word_dict[w] = {"spam_count": 1, "ham_count": 0}
                    wordcount_spam += 1

    vocabulary_size = len(word_dict)
    print("Vocabulary Size:" + str(vocabulary_size))
    print("spam file count :" + str(spam_file_count))
    print("ham file count :" + str(ham_file_count))
    # print("unique words in spam:" + str(len(spam_dict)))
    # print("unique words in ham:" + str(len(ham_dict)))
    print("Total Words in Spam:" + str(wordcount_spam))
    print("Total Words in ham:" + str(wordcount_ham))

    # print(spam_dict.keys())

    # serializing the data
    obj = Model(vocabulary_size, spam_file_count, ham_file_count, wordcount_spam, wordcount_ham, word_dict)
    a = json.dumps(vars(obj))
    fs = open("nbmodel.txt", "w")
    fs.write(a)

if __name__ == "__main__": main()


# /Users/abhinavkumar/Desktop/USC/Courses_Fall2016/CSCI544_HW/Ass1/Spam\ or\ Ham/train