from nltk.corpus import wordnet
import warnings

class HierarchicalMetrics:
    def __init__(self):
        # Suppress UserWarnings from NLTK WordNet module
        warnings.filterwarnings("ignore", category=UserWarning, module="nltk.corpus.reader.wordnet")

    def specialization_hierarchy(self, word1, word2):  # top_down_relationship
        synsets_word1 = wordnet.synsets(word1)
        synsets_word2 = wordnet.synsets(word2)

        for syn1 in synsets_word1:
            for syn2 in synsets_word2:
                if syn1 == syn2:
                    continue  # Skip identical synsets

                if syn1 in syn2.closure(lambda s: s.hypernyms()):
                    #print(f"{word1} is a specialization of {word2}")
                    return True

                if syn2 in syn1.closure(lambda s: s.hypernyms()):
                    #print(f"{word2} is a specialization of {word1}")
                    return True

        #print(f"No top-down relationship found between {word1} and {word2}")
        return False

    def reversed_hierarchy(self, word1, word2):  # down_top_relationship
        synsets_word1 = wordnet.synsets(word1)
        synsets_word2 = wordnet.synsets(word2)

        for syn1 in synsets_word1:
            for syn2 in synsets_word2:
                if syn1 == syn2:
                    continue  # Skip identical synsets

                if syn1 in syn2.closure(lambda s: s.hyponyms()):
                    #print(f"{word1} is a broader category of {word2}")
                    return True

                if syn2 in syn1.closure(lambda s: s.hyponyms()):
                    #print(f"{word2} is a broader category of {word1}")
                    return True

        #print(f"No down-top relationship found between {word1} and {word2}")
        return False

