class Trie:
    def __init__(self):
        self.children = {}
        self.end_of_a_word = False
        self.suffix_link = None


def build_trie(keywords):
    root = Trie()

    for keyword in keywords:
        node = root
        for letter in keyword:
            node = node.children.setdefault(letter, Trie())
        node.end_of_a_word = True

    return root


def build_suffix_link(root):
    queue = []

    for child in root.children.values():
        child.suffix_link = root
        queue.append(child)

    while queue:
        current_node = queue.pop(0)

        for letter, child in current_node.children.items():
            queue.append(child)
            suffix_link_node = current_node.suffix_link

            while suffix_link_node is not None and letter not in suffix_link_node.children:
                suffix_link_node = suffix_link_node.suffix_link

            child.suffix_link = suffix_link_node.children.get(letter) if suffix_link_node and suffix_link_node.children else root



def search_patterns(txt, root):
    patterns = []
    current_node = root
    compressed_links = {}

    for i, letter in enumerate(txt):
        while current_node is not None and letter not in current_node.children:
            current_node = current_node.suffix_link

        if current_node is None:
            current_node = root
            continue

        current_node = current_node.children[letter]

        if current_node.end_of_a_word:
            for j in range(len(keywords)):
                if txt[i - len(keywords[j]) + 1: i + 1] == keywords[j]:
                    patterns.append((i - len(keywords[j]) + 1, keywords[j]))
        
        compressed_link = compressed_links.get(current_node)
        if compressed_link is not None:
            current_node = compressed_link

    return patterns


def aho_corasick(txt, keywords):
    root = build_trie(keywords)
    build_suffix_link(root)
    patterns = search_patterns(txt, root)
    return patterns


with open("Desktop/aho_corasick/voina_mir.txt", "r", encoding="utf-8") as file: # here you can provide your own txt file. Make sure that you include the whole path to the file
    txt = file.read()

keywords = ["Он", "дети", "Между", "мой"] # here you can write your own keywords
result = aho_corasick(txt, keywords)

if result:
    print("Following matches were found:")
    for pos, keyword in result:
        print(f"The word '{keyword}' was found in a position of {pos}")
else:
    print("The matches were not found")
