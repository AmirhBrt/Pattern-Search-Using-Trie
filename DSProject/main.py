import heapq
import re
import time


class Node:
    def __init__(self, char, word=None):
        self.children = dict()
        self.char = char
        self.word = word
        self.isEndOfWord = False
        self.file_to_value = dict()


class Trie:

    def __init__(self):
        self.root = Node(char=None)

    def insert(self, word, main_word, file_num):
        temp_node = self.root
        for i in range(len(word)):
            if word[i] not in temp_node.children:
                temp_node.children[word[i]] = Node(word[i])
            temp_node = temp_node.children[word[i]]
        temp_node.isEndOfWord = True
        temp_node.word = main_word
        if file_num not in temp_node.file_to_value:
            temp_node.file_to_value[file_num] = 1
        else:
            temp_node.file_to_value[file_num] += 1

    def search(self, pattern) -> dict:
        temp_node = self.root
        index = 0
        while index < len(pattern) - 1:
            char = pattern[index]
            if char in temp_node.children:
                temp_node = temp_node.children[char]
                index += 1
            else:
                return dict()
        return self.get_word_children(temp_node)

    def get_word_children(self, temp_node: Node) -> dict:
        file_to_num = dict()
        if temp_node.isEndOfWord:
            for key in temp_node.file_to_value:
                file_to_num[key] = temp_node.file_to_value[key]
        for child in temp_node.children:
            tmp_file_to_num = self.get_word_children(temp_node.children[child])
            for key in tmp_file_to_num:
                if key not in file_to_num:
                    file_to_num[key] = tmp_file_to_num[key]
                else:
                    file_to_num[key] += tmp_file_to_num[key]
        return file_to_num


def left_rotate(word, count):
    return word[count:] + word[:count]


def insert_all(trie, word_num):
    words = input().split()
    for i in range(word_num):
        words[i] = words[i].lower()
        temp_word = words[i]
        temp_word += '$'
        for j in range(len(temp_word)):
            trie.insert(temp_word, words[i])
            temp_word = left_rotate(temp_word, 1)


def replace_invalids(word: str):
    word = word.lower()
    if not bool(re.match('^[a-z0-9]+$', word)):
        word = re.sub('\W|_', '', word)
    return word


def insert_word_to_trie(trie: Trie, i: int, word: str):
    temp_word = word
    temp_word += '$'
    for j in range(len(temp_word)):
        trie.insert(temp_word, word, i)
        temp_word = left_rotate(temp_word, 1)


def insert_file_to_trie(trie: Trie, file, i):
    for line in file:
        if line == '':
            continue
        for word in line.split():
            word = replace_invalids(word)
            if word == '':
                continue
            insert_word_to_trie(trie, i, word)


def insert_files(trie: Trie):
    for i in range(10):
        if i == 9:
            file = open('./docs/doc10.txt', 'r+')
        else:
            file = open('./docs/doc0' + str(i + 1) + '.txt', 'r+')
        insert_file_to_trie(trie, file, i + 1)
        file.close()


def handle_queries(input_file, queries, result_file, trie):
    start_time = time.time()
    for i in range(queries):
        pattern = input_file.readline()
        pattern = re.sub('\\\n', '', pattern)
        pattern = re.sub('\\\\S', '', pattern)
        pattern += '$'
        index = pattern.find('*')
        pattern = left_rotate(pattern, index + 1)
        file_to_num = trie.search(pattern)
        if len(file_to_num) == 0:
            result_file.write('-1\n')
        else:
            ans = ''
            heap = []
            heapq.heapify(heap)
            for key in file_to_num:
                heapq.heappush(heap, (-file_to_num[key], key))
            while heap:
                item = heapq.heappop(heap)
                ans += str(item[1]) + ' '
            ans = ans.strip()
            result_file.write(ans + '\n')
    end_time = time.time()
    return end_time, start_time


def search_files(trie):
    input_file = open('input.txt', 'r+')
    result_file = open('result.txt', 'w+')
    time_file = open('time.txt', 'w+')
    queries = input_file.readline()
    queries = int(queries)
    end_time, start_time = handle_queries(input_file, queries, result_file, trie)
    duration = end_time - start_time
    time_file.write(str(duration))
    time_file.close()
    input_file.close()
    result_file.close()


def main():
    trie = Trie()
    insert_files(trie)
    search_files(trie)


if __name__ == '__main__':
    main()
