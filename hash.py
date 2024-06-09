import re
from collections import Counter

class HashTable:
    def __init__(self, initial_capacity=8):
        self.table = [[] for _ in range(initial_capacity)]
        self.size = 0
        self.capacity = initial_capacity
        self.load_factor_threshold = 0.75

    def hash_function(self, key):
        return hash(key) % self.capacity

    def insert(self, key, value):
        index = self.hash_function(key)
        for pair in self.table[index]:
            if pair[0] == key:
                pair[1] = value
                return
        self.table[index].append([key, value])
        self.size += 1

        if self.size / self.capacity > self.load_factor_threshold:
            self.resize()

    def get(self, key):
        index = self.hash_function(key)
        for pair in self.table[index]:
            if pair[0] == key:
                return pair[1]
        return None

    def remove(self, key):
        index = self.hash_function(key)
        for i, pair in enumerate(self.table[index]):
            if pair[0] == key:
                del self.table[index][i]
                self.size -= 1
                return
        return None

    def resize(self):
        new_capacity = self.capacity * 2
        new_table = [[] for _ in range(new_capacity)]

        for bucket in self.table:
            for key, value in bucket:
                new_index = hash(key) % new_capacity
                new_table[new_index].append([key, value])

        self.table = new_table
        self.capacity = new_capacity

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    words = text.split()
    return words

def count_word_frequencies(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    words = preprocess_text(text)
    word_count = HashTable()

    for word in words:
        count = word_count.get(word)
        if count is None:
            word_count.insert(word, 1)
        else:
            word_count.insert(word, count + 1)

    return word_count

def get_top_n_frequencies(word_count, n=10):
    word_list = []
    for bucket in word_count.table:
        for key, value in bucket:
            word_list.append((key, value))

    word_list.sort(key=lambda x: x[1], reverse=True)
    return word_list[:n]

file_path = 'text.txt'
word_count = count_word_frequencies(file_path)
top_words = get_top_n_frequencies(word_count)

print("Top 10 most frequent words:")
for word, frequency in top_words:
    print(f"{word}: {frequency}")