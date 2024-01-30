import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from file_handler import FileReadWrite
import spacy

#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('wordnet')


class UriCleaning:
    def __init__(self):
        self.Uri =  None
        path = "acronyms.txt"
        with open(path, 'r') as f:
            self.acronym = f.read()
        
        

    def get_uri_nodes(self, Uri):

        extensions = [".json", ".html", ".pdf", ".txt", ".xml", ".jpg", ".jpeg", ".png", ".gif", ".csv", ".htm", ".zip"]

        pattern = re.compile('|'.join([re.escape(ext) for ext in extensions]))
        Uri = pattern.sub(' ', Uri)
        #print(Uri)

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


        #print(uri_nodes)
        res = []
        for item in uri_nodes:
            found = False
            for line in self.acronym.split("\n"):
                line_parts = line.split(">>")
                if line_parts[0].strip() == item.strip().lower():
                    #print(f"{line_parts[0]}--------------{item}")
                    res.extend(line_parts[1].strip().split())
                    found = True
                    break
            if not found:
                res.append(item)
        #print(res)


        # Tokenize the words and filter out stop words and numeric values
        tokenized_uri = word_tokenize(" ".join(res))
        uri_nodes = [word for word in tokenized_uri if word not in stop_words and not word.isdigit()]
        tokens = [token for token in uri_nodes if len(token) > 1] #get rid of single characters
        return tokens
    
    def preprocess_documentation(self, text):
        text = text.replace('n/a','').replace('REQUIRED','').replace('Required','').replace('String','')
        extensions = [".json", ".html", ".pdf", ".txt", ".xml", ".jpg", ".jpeg", ".png", ".gif", ".csv", ".htm", ".zip"]
        pattern = re.compile('|'.join([re.escape(ext) for ext in extensions]))
        doc = pattern.sub(' ', text)
        
        #print(doc)
        
        clean_doc = ""
        if "?" in doc:
            clean_doc = doc[:doc.index("?")]
        else:
            clean_doc = doc
        if "_" in clean_doc or "-" in clean_doc or "/" in clean_doc:
            clean_doc = clean_doc.replace("_", " ").replace("-", " ").replace("/"," ")
        else:
            clean_doc = clean_doc
        #clean_uri.append(ur)
        #print(clean_doc)
        
        doc = re.sub(r'[^a-zA-Z0-9\s]', '', clean_doc)
        #print(doc)
        docu = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', doc)
        #print(docu)
        tokens = []
        for d in docu:
            if d in ['may','might','will','would','shall', 'should', 'www', 'com', 'true', 'false', 'link','https']:
                continue
            tokens.append(d.strip().lower())
        #print(tokens)        
        #set acronhym
        #tokens = self.get_Acronym(tokens)    
        res = []
        for item in tokens:
            found = False
            for line in self.acronym.split("\n"):
                line_parts = line.split(">>")
                if line_parts[0].strip() == item.strip().lower():
                    #print(f"{line_parts[0]}--------------{item}")
                    res.extend(line_parts[1].strip().split())
                    found = True
                    break
            if not found:
                res.append(item)
        #print(res)
        nlp = spacy.load("en_core_web_lg")
        stop_words = set(stopwords.words('english'))


        tokens = word_tokenize(" ".join(res))
        tokens = [token for token in tokens if token.isalpha() and token not in stop_words]
        dod = tokens
        doc = nlp(" ".join(tokens))
        lemmatized_tokens = [token.lemma_ for token in doc]
        tokens = [token for token in lemmatized_tokens if len(token) > 1]
        return tokens
        
    def set_Acronym(self, text):
        path = "acronyms.txt"

        read_data = FileReadWrite(path)
        data = read_data.read_data()
        #print(data)

        for line in data:
            line  = line.split(">>")
            line[1].strip("\n")
            if(text.lower() == line[0].strip().lower()):
                ret = line[1].strip()
                ret = ret.split()
                return ret
    
    def get_Acronym(self, lst):
        #path = "acronyms.txt"
        #with open(path, 'r') as f:
            #acronym = f.read()
            #print(acronym)
        res = []
        for item in lst:
            found = False
            for line in self.acronym.split("\n"):
                line_parts = line.split(">>")
                if line_parts[0].strip() == item.strip().lower():
                    #print(f"{line_parts[0]}--------------{item}")
                    res.extend(line_parts[1].strip().split())
                    found = True
                    break
            if not found:
                res.append(item)
        return res
                

    