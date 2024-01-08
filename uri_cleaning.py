import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


class UriCleaning:
    def __init__(self):
        self.Uri =  None

    def get_uri_nodes(self, Uri):
        #Uri = Uri if Uri else self.Uri
        stop_words = set(stopwords.words('english'))
        #print(Uri)
        clean_uri = ""
        if "?" in Uri:
            clean_uri = Uri[:Uri.index("?")]
        else:
            clean_uri = Uri
        if "_" in clean_uri or "-" in clean_uri:
            clean_uri = clean_uri.replace("_", " ").replace("-", " ")
        else:
            clean_uri = clean_uri
        #clean_uri.append(ur)
        #print(clean_uri)
        tmp = []
        words = clean_uri.split("/")
        for word in words:
                if len(word) > 2:
                    tmp.append(word)
        #print(tmp)
        #words = clean_uri.split("/")
        nodes = []
        for n in tmp:
            nodes.append(re.sub(r'[^a-zA-Z0-9\s]', '', n))
        #print(nodes)
        splitted_nodes = []
        for node in nodes:
            tmp1 = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', node)
            splitted_nodes.extend(tmp1)
        #print(splitted_nodes)
        uri_nodes = []
        for Node in splitted_nodes:
            Node = Node.strip().lower()
            split_nodes = [word.lower().strip() for word in Node.split('_') if word]
            uri_nodes.extend(split_nodes)
        # Tokenize the words and filter out stop words and numeric values
        tokenized_uri = word_tokenize(" ".join(uri_nodes))
        uri_nodes = [word for word in tokenized_uri if word not in stop_words and not word.isdigit()]
        return uri_nodes
    