from uri_cleaning import UriCleaning
from hierarchical_metrics import HierarchicalMetrics
import re
import nltk
from nltk.stem import WordNetLemmatizer #for pluralized nodes
from nltk.corpus import wordnet as wn #for nondescritive URI
#nltk.download('wordnet')  # Download WordNet data if not downloaded
#nltk.download('stopwords')
#nltk.download('punkt')
import gensim
from gensim import corpora
from gensim.models import LdaModel
from gensim.models.coherencemodel import CoherenceModel
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import spacy
from collections import defaultdict
from itertools import combinations
from sklearn.metrics.pairwise import cosine_similarity
from tabulate import tabulate
import warnings
#import math
#import csv
import json
import inflect 
    

class ApiAnalyzer:
    def __init__(self, api_type, api):
        #self.URI = URI
        self.api_type = api_type
        self.api_name = api
        warnings.filterwarnings("ignore", category=UserWarning)
        self.description = []
        self.nodes = []
        self.http_method = []
        self.id = []
        
        path = 'All-Data\Alldata.jsonl'
        with open(path, 'r') as file:
            lines = file.read().strip().split("\n")
            for line in lines:
                row = json.loads(line)
                #print(row)

                #if len(line) == 7:
                    #id, apis_type, api_name, verb, uri, des, para = line[0], line[1], line[2], line[3], line[4], line[5], line[6]
                #else:
                    #id, apis_type, api_name, verb, uri, des, para = line[0], line[1], line[2], line[3], line[4], line[5], ''
            
                if row["api_type"] == api_type and row["api_name"] == api:
                    #self.id.append(row["id"])
                    self.description.append(row["description"] + row["parameters"])
                    #self.nodes.append(row["uri"])
                    #self.http_method.append(row["method"])
        

        self.clean = UriCleaning()
        #splitted_nodes = clean.get_uri_nodes(line)

        self.processed_des =[]
        for des in self.description:
            self.processed_des.append(self.clean.preprocess_documentation(des))
        '''self.processed_nodes =[]
        for nd in self.nodes:
            self.processed_nodes.append(self.clean.get_uri_nodes(nd))'''

        #self.clean_description = extend(processed_des)
        



    def detect_amorphous_uri(self):
        P = "Tidy End-point"
        AP = "Amorphous End-point"
        found_AP = 0
        p_count = 0
        ap_count = 0
        amorphus_result_AP = []
        amorphus_result_P = []
        extensions = [".json", ".html", ".pdf", ".txt", ".xml", ".jpg", ".jpeg", ".png", ".gif", ".csv", ".htm", ".zip"]
        def has_consecutive_uppercase(s):
            for i in range(len(s)-1):
                if s[i].isupper() and s[i+1].isupper():
                    return True
            return False
        def is_camel_case(s):
            s = ''.join(i for i in s if not i.isdigit())
            #print(s)
            flag = 'False'
            if s != s.lower() and s != s.upper() and has_consecutive_uppercase(s): #has_consecutive_uppercase
                flag = 'False'   
            elif s != s.lower() and s != s.upper() and "_" not in s and sum(i.isupper() for i in s) == 1: 
                if s[0].isupper():
                    flag = 'False'
                elif s[0].islower():
                    flag = 'True'
            elif s != s.lower() and s != s.upper() and "_" not in s and sum(i.isupper() for i in s) >= 1:
                flag = 'True'
            return flag
        
        path = 'All-Data\Alldata.jsonl'
        with open(path, 'r+') as file:
            lines = file.read().strip().split("\n")
            file.seek(0)
            for line in lines:
                row = json.loads(line)
                if row["api_type"] == self.api_type and row["api_name"] == self.api_name:
                    uris = row['uri']
                    words = uris.strip().split("/")
                    comment = ""
                    found_AP = 0

                    for word in words:
                        word = word.strip()
                        word = word.replace("<", '').replace(">", '') #replace("{", '').replace("}",'')
                        flag = 0
                        if word: 
                            if word[0].strip() == "{" and word[-1].strip() == "}":
                                #print("variable")
                                continue
                            elif any(ch.isupper() for ch in word) and is_camel_case(word) == "False":
                                found_AP = 1
                                comment += " [uppercase found] "
                                flag = 1
                            
                            elif "%5F" in word.lower() or "%5F" in word or "_" in word:
                                found_AP = 1
                                comment += " [underscore found] "
                                flag = 1
                            elif uris.strip()[-1] == '/' or uris.strip()[-1] == '\\':
                                found_AP = 1
                                comment += " [trailing slash found] "
                                flag = 1
                            else:
                                for extension in extensions:
                                    if extension.lower() in uris.lower() or extension.upper() in uris:
                                        found_AP = 1
                                        comment += " [extension found] "
                                        flag = 1
                        if flag == 1:
                            break
                    if found_AP == 1:
                            row['amorphous_uri'] = 1
                            row['tidy_uri'] = 0
                            ap_count = ap_count + 1
                            amorphus_result_AP.append(uris.strip() + "\t" + AP + "\t" + comment)
                    else:
                            row['amorphous_uri'] = 0
                            row['tidy_uri'] = 1
                            p_count = p_count + 1
                            comment = "Tidy Endpoint"
                            amorphus_result_P.append(uris.strip() + "\t" + P + "\t" + comment)
                    row['amorphous_comment'] = comment
                    print("->", end=" ")

                json_string=json.dumps(row, ensure_ascii=False)
                file.write(json_string+"\n")     
                
        return amorphus_result_AP, amorphus_result_P, p_count, ap_count
    




    def detect_non_standard_uri(self):
        P = "Standard End-point"
        AP = "Non-standard End-point"
        standard_uri_result_AP = []
        standard_uri_result_P = []
        p_count = 0
        ap_count = 0
        # Common European languages
        european_languages = [
            # French
            'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç', 'È', 'É', 'Ê', 'Ë', 'Ì', 'Í', 'Î', 'Ï', 'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', 'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'à', 'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î', 'ï', 'ð', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', 'ø', 'ù', 'ú', 'û', 'ü', 'ý', 'ÿ', 'Œ', 'œ',

            # Italian
            'Ā', 'Ă', 'Ą', 'Ć', 'Ĉ', 'Ċ', 'Č', 'Ď', 'Đ', 'Ē', 'Ĕ', 'Ė', 'Ę', 'Ě', 'Ĝ', 'Ğ', 'Ġ', 'Ģ', 'Ĥ', 'Ħ', 'Ĩ', 'Ī', 'Ĭ', 'Į', 'İ', 'Ĳ', 'Ĵ', 'Ķ', 'Ĺ', 'Ļ', 'Ľ', 'Ŀ', 'Ł', 'Ń', 'Ņ', 'Ň', 'Ŋ', 'Ō', 'Ŏ', 'Ő', 'Œ', 'Ŕ', 'Ŗ', 'Ř', 'Ś', 'Ŝ', 'Ş', 'Š', 'Ţ', 'Ť', 'Ŧ', 'Ũ', 'Ū', 'Ŭ', 'Ů', 'Ű', 'Ų', 'Ŵ', 'Ŷ', 'Ÿ', 'Ź', 'Ż', 'Ž',

            # Spanish
            'Á', 'É', 'Í', 'Ñ', 'Ó', 'Ú', 'Ü', 'á', 'é', 'í', 'ñ', 'ó', 'ú', 'ü',

            # German
            'Ä', 'Ö', 'Ü', 'ä', 'ö', 'ü', 'ß',

            # Portuguese
            'Á', 'Â', 'Ã', 'À', 'Ç', 'É', 'Ê', 'Í', 'Õ', 'Ó', 'Ô', 'Ú', 'á', 'â', 'ã', 'à', 'ç', 'é', 'ê', 'í', 'õ', 'ó', 'ô', 'ú',

            # Dutch
            'Ĳ', 'ĳ',

            # Czech
            'Č', 'č', 'Ď', 'ď', 'Ě', 'ě', 'Ň', 'ň', 'Ř', 'ř', 'Š', 'š', 'Ť', 'ť', 'Ů', 'ů', 'Ž', 'ž'
        ]
        # Cyrillic languages
        cyrillic_languages = [
            # Russian
            'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я',

            # Bulgarian
            'Й', 'Ъ', 'Ь', 'ё', 'й', 'ъ', 'ь'
        ]
        # Greek
        greek_language = [
            'Α', 'Β', 'Γ', 'Δ', 'Ε', 'Ζ', 'Η', 'Θ', 'Ι', 'Κ', 'Λ', 'Μ', 'Ν', 'Ξ', 'Ο', 'Π', 'Ρ', 'Σ', 'Τ', 'Υ', 'Φ', 'Χ', 'Ψ', 'Ω',
            'α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'τ', 'υ', 'φ', 'χ', 'ψ', 'ω'
        ]
        # Arabic
        arabic_language = [
            'ا', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'و', 'ي'
        ]
        # Japanese
        japanese_language = [
            'あ', 'い', 'う', 'え', 'お', 'か', 'き', 'く', 'け', 'こ', 'さ', 'し', 'す', 'せ', 'そ', 'た', 'ち', 'つ', 'て', 'と', 'な', 'に', 'ぬ', 'ね', 'の', 'は', 'ひ', 'ふ', 'へ', 'ほ', 'ま', 'み', 'む', 'め', 'も', 'や', 'ゆ', 'よ', 'ら', 'り', 'る', 'れ', 'ろ', 'わ', 'を', 'ん'
        ]
        #unknown_characters = ['!', '@', '#', '$', '~', '^', '*', '>', '<', '|', '%', '&', '+', '=', '`', '?', ',', ';', ':', '.']

        #for method, uris, doc in zip(self.http_method, self.nodes, self.description):
        path = 'All-Data\Alldata.jsonl'
        with open(path, 'r+') as file:
            lines = file.read().strip().split("\n")
            file.seek(0)
            for line in lines:
                row = json.loads(line)
                if row["api_type"] == self.api_type and row["api_name"] == self.api_name:
                    uri = row['uri']
                    comment = ""
                    found_AP = 0
                    uri = uri.strip()
                    if any(c in uri.lower() for c in european_languages):
                        found_AP = 1
                        comment += " [european char found] "
                    elif any(c in uri.lower() for c in cyrillic_languages):
                        found_AP = 1
                        comment += " [ cyrillic char found] "
                    elif any(c in uri.lower() for c in greek_language):
                        found_AP = 1
                        comment += " [ greek char found] "
                    elif any(c in uri.lower() for c in arabic_language):
                        found_AP = 1
                        comment += " [ arabic char found] "
                    elif any(c in uri.lower() for c in japanese_language):
                        found_AP = 1
                        comment += " [ japanese char found] "
                    elif ' ' in uri.strip() or '\t' in line.strip():
                        found_AP = 1
                        comment += " [blank space/tab found] "
                    elif '--' in uri:
                        found_AP = 1
                        comment += " [double hyphens found] "
                    elif any(c in uri.lower() for c in ['!', '@', '#', '$', '~', '^', '*', '>', '<']):
                        found_AP = 1
                        comment += " [unknown char found] "

                    if found_AP == 1:
                        row['non_standard_uri'] = 1
                        row['standard_uri'] = 0
                        standard_uri_result_AP.append(f"{uri.strip()}\t{AP}\t{comment}")
                        ap_count += 1
                    else:
                        row['non_standard_uri'] = 0
                        row['standard_uri'] = 1
                        comment = "Standard Endpoint"
                        standard_uri_result_P.append(f"{uri.strip()}\t{P}\t{comment}")
                        p_count += 1
                    row['non_standard_comment'] = comment
                    print("->", end=" ")
                
                json_string=json.dumps(row, ensure_ascii=False)
                file.write(json_string+"\n")

        return standard_uri_result_AP, standard_uri_result_P, p_count, ap_count
    
    

    def detect_crudy_uri(self):
        P = "Verbless End-point"
        AP = "CRUDy End-point"
        crudyWords = ["create", "make", "write", "read", "search", "show", "take", "delete", "destroy", "cancel", "remove", "update", "copy", "move", "upgrade", "notify"]
        crudyURIResult_AP = []
        crudyURIResult_P = []
        p_count = 0
        ap_count = 0

        path = 'All-Data\Alldata.jsonl'
        with open(path, 'r+') as file:
            lines = file.read().strip().split("\n")
            file.seek(0)
            for line in lines:
                row = json.loads(line)
                if row["api_type"] == self.api_type and row["api_name"] == self.api_name:
                    uris = row['uri']
                    method = row['method']
                    nodes = self.clean.get_uri_nodes(uris)
        
                #for method, nodes, uris, doc in zip(self.http_method, self.processed_nodes, self.nodes, self.description):
                    #tmp = ur.strip().split(">>")
                    #print(tmp)

                    good_type = False
                    comment = ""
                    ap_found = False
                    
                    if len(nodes) < 1:
                        good_type = True
                    # Check if any CRUDy word is found in the URI
                    for node_word in nodes:
                        for crudy_word in crudyWords:
                            if node_word.lower() == crudy_word.lower():
                                good_type = False
                                ap_found = True
                                comment += f" [{crudy_word} found] "
                                break
                            else:
                                good_type = True

                        if ap_found:
                            break

                    if not good_type:
                        row['crudy_uri'] = 1
                        row['verbless_uri'] = 0
                        ap_count = ap_count + 1
                        crudyURIResult_AP.append(f"{uris.strip()}\t{AP}\t{comment}")
                    else:
                        row['crudy_uri'] = 0
                        row['verbless_uri'] = 1
                        p_count = p_count + 1
                        crudyURIResult_P.append(f"{uris.strip()}\t{P}\t{comment}")
                    row['crudy_comment']
                    print("->", end=" ")
                json_string=json.dumps(row, ensure_ascii=False)
                file.write(json_string+"\n")

        return crudyURIResult_AP, crudyURIResult_P, p_count, ap_count
    
    

    def detect_unversioned_uris(self):
        versioned_result_P = []
        unversioned_result_AP = []
        p_count = 0
        ap_count = 0
        #print(URI)
        #for method, uris, doc in zip(self.http_method, self.nodes, self.description):
        path = 'All-Data\Alldata.jsonl'
        with open(path, 'r+') as file:
            lines = file.read().strip().split("\n")
            file.seek(0)
            for line in lines:
                row = json.loads(line)
                if row["api_type"] == self.api_type and row["api_name"] == self.api_name:
                    uris = row['uri']
                    regex_list = [
                        ".*v\d+.*",         # Matches any string containing "v" followed by digits
                        ".*v\d+.*",         # Matches any string containing "v" followed by digits
                        ".*v\d+.*",         # Matches any string containing "v" followed by digits
                        ".*v\d+.*",         # Matches any string containing "v" followed by digits
                        ".*v\d+.*",         # Matches any string containing "v" followed by digits
                        ".*/v/.*",          # Matches any string containing "/v/"
                        ".*api-version=.*", # Matches any string containing "api-version="
                        "/v\d+\.\d+/",      # Matches "/v" followed by digits, a dot, and more digits
                        "/v\d+\.\d+/"       # Matches "/v" followed by digits, a dot, and more digits
                    ]
                    matches = any(re.match(regex, uris) for regex in regex_list)

                    if matches:
                        row['unversioned_uri'] = 1
                        row['versioned_uri'] = 0
                        comment = "Version Found"
                        versioned_result_P.append(f"{uris.strip()} \t {comment}")
                        p_count += 1
                    else:
                        row['unversioned_uri'] = 1
                        row['versioned_uri'] = 0
                        comment = "No Version Found"
                        unversioned_result_AP.append(f"{uris.strip()} \t {comment}")
                        ap_count += 1
                    row['unversioned_comment'] = comment
                    print("->", end=" ")
                json_string = json.dumps(row, ensure_ascii=False)
                file.write(json_string+"\n")
                
        return unversioned_result_AP, versioned_result_P , p_count, ap_count


    def detect_pluralized_node(self):
        pluralised_result_AP = []
        pluralised_result_P = []
        P = "Singularized Nodes"
        AP = "Pluralized Nodes"
        p_count = 0
        ap_count = 0
    
        def is_plural(word):
            lemmatizer = WordNetLemmatizer()
            lemma = lemmatizer.lemmatize(word, pos='n')
            return word != lemma
        #print(is_plural("sources"))

        #for method, uris, nodes, doc in zip(self.http_method, self.nodes, self.processed_nodes, self.description):
        path = 'All-Data\Alldata.jsonl'
        with open(path, 'r+') as file:
            lines = file.read().strip().split("\n")
            file.seek(0)
            for line in lines:
                row = json.loads(line)
                if row["api_type"] == self.api_type and row["api_name"] == self.api_name:
                    uris = row['uri']  
                    method = row['method']
                    nodes = self.clean.get_uri_nodes(uris)
                    comment1 = "Singular last node with POST method"
                    comment2 = "Pluralized last node with POST method"
                    comment3 = "Pluralized last node with PUT and DELETE method"
                    comment4 = "Singular last node with PUT and DELETE method"
                    comment5 = "Regular methods"

                    #if no nodes in uri
                    #print(nodes)
                    if len(nodes) < 1:
                        row['pluralized_nodes'] = 0
                        row['singularized_nodes'] = 1
                        row['pluralized_comment'] = comment5
                        p_count += 1
                        pluralised_result_P.append(f"{method}\t{uris.strip()}\t{P}\t {comment5}")
                        continue
                    last_node = nodes[-1]

                    if method.strip() == "POST":
                        if is_plural(last_node):
                            p_count += 1
                            row['pluralized_nodes'] = 0
                            row['singularized_nodes'] = 1
                            row['pluralized_comment'] = comment2
                            pluralised_result_P.append(f"{method}\t{uris.strip()}\t{P}\t{comment2}")
                        else:
                            row['pluralized_nodes'] = 1
                            row['singularized_nodes'] = 0
                            row['pluralized_comment'] = comment1
                            ap_count += 1
                            pluralised_result_AP.append(f"{method}\t{uris.strip()}\t{AP}\t{comment1}")

                    elif method.strip() == "DELETE" or method.strip() == "PUT":
                        if is_plural(last_node):
                            row['pluralized_nodes'] = 1
                            row['singularized_nodes'] = 0
                            row['pluralized_comment'] = comment3
                            ap_count += 1
                            pluralised_result_AP.append(f"{method}\t{uris.strip()}\t{AP}\t{comment3}")
                        else:
                            row['pluralized_nodes'] = 0
                            row['singularized_nodes'] = 1
                            row['pluralized_comment'] = comment4
                            p_count += 1
                            pluralised_result_P.append(f"{method}\t{uris.strip()}\t{P}\t{comment4}")
                    else:
                        row['pluralized_nodes'] = 0
                        row['singularized_nodes'] = 1
                        row['pluralized_comment'] = comment5    
                        p_count += 1
                        pluralised_result_P.append(f"{method}\t{uris.strip()}\t {comment5}")
                    print("->", end=" ")
                json_string = json.dumps(row, ensure_ascii=False)
                file.write(json_string+"\n")
        return pluralised_result_AP, pluralised_result_P, p_count, ap_count
    

    def detect_non_descriptive_uri(self):
        non_descriptive_AP = []
        self_descriptive_P = []
        P = "Self-descriptive End-point"
        AP = "Non-descriptive End-point"
        p_count = 0
        ap_count = 0


        #for method, uris,nodes, doc in zip(self.http_method, self.nodes, self.processed_nodes, self.description):
        path = 'All-Data\Alldata.jsonl'
        with open(path, 'r+') as file:
            lines = file.read().strip().split("\n")
            file.seek(0)
            for line in lines:
                row = json.loads(line)
                if row["api_type"] == self.api_type and row["api_name"] == self.api_name:
                    uris = row['uri']  
                    #method = row['method']
                    nodes = self.clean.get_uri_nodes(uris)
        
                    pattern = True

                    for word in nodes:
                        # Perform word lookup operation
                        synsets = wn.synsets(word.strip())
                        
                        if synsets:
                            pattern = pattern | True
                        else:
                            pattern = pattern & False

                    if not pattern:
                        row['non_descriptive_uri'] = 1
                        row['descriptive_uri'] = 0
                        row['non_descriptive_comment'] = AP
                        ap_count = ap_count + 1
                        non_descriptive_AP.append(f"{uris.strip()}\t {AP}")
                    elif pattern:
                        row['non_descriptive_uri'] = 0
                        row['descriptive_uri'] = 1
                        row['non_descriptive_comment'] = P
                        p_count = p_count + 1
                        self_descriptive_P.append(f"{uris.strip()}\t {P}")                    
                    print("->", end=" ")
                json_string = json.dumps(row, ensure_ascii=False)
                file.write(json_string+"\n")

        return non_descriptive_AP, self_descriptive_P, p_count, ap_count
    

    def detect_contextless(self):
        contextless_AP = []
        contextual_P = []
        P = "Contextual Resource Names"
        AP = "Contextless Resource Names"
        p_count = 0
        ap_count = 0
        # Tokenize, remove stopwords, and lemmatize the descriptions
        nlp = spacy.load("en_core_web_lg")
        #stop_words = set(stopwords.words('english'))


        def preprocess_word(text):
            doc = nlp(text)
            tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
            return ' '.join(tokens)

        def similarity_calculator(word1, word2):
            word1 = nlp(preprocess_word(word1))
            word2 = nlp(preprocess_word(word2))
            simi = word1.similarity(word2)
            return simi

        # Create a dictionary and corpus for LDA modeling
        #print(self.processed_des)
        dictionary = corpora.Dictionary(self.processed_des)
        corpus = [dictionary.doc2bow(text) for text in self.processed_des]

        # Train LDA model
        lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=5, random_state=42)

        # Get topic words from the model
        topic_words = []
        for topic_id in range(lda_model.num_topics):
            topic_words.append([word for word, _ in lda_model.show_topic(topic_id)])
        #print(topic_words)

        # Display topic words horizontally
        '''table = [["Topic " + str(i+1)] + words for i, words in enumerate(topic_words)]
        print(tabulate(table, headers="firstrow", tablefmt="grid"))'''

        def calculate_similarity(uri_node, topic_words):
            similarity_scores = {}
            for idx, word_list in enumerate(topic_words, start=1):
                word_similarity = {word: similarity_calculator(uri_node, word) for word in word_list}
                similarity_scores[f"Topic {idx}"] = word_similarity
            return similarity_scores

        #for method, combined_node, origianl_node, des in zip(self.http_method, self.processed_nodes, self.nodes, self.description):
            #print(f"{method}---{combined_node}---{des}")
        path = 'All-Data\Alldata.jsonl'
        with open(path, 'r+') as file:
            lines = file.read().strip().split("\n")
            file.seek(0)
            for line in lines:
                row = json.loads(line)
                if row["api_type"] == self.api_type and row["api_name"] == self.api_name:
                    uris = row['uri']  
                    method = row['method']
                    des = row['description']
                    combined_node = self.clean.get_uri_nodes(uris)
        
                    if len(combined_node)<1:
                        row['contextless_resource'] = 0
                        row['contextual_resouce'] = 1
                        row['contextless_comment'] = P
                        p_count = p_count + 1
                        contextual_P.append(f"-{uris}\t{P}")
                        continue
                    # Calculate similarity for each individual node
                    node_word_similarity = {}
                    topic_avg = []
                    for node in combined_node:
                        node_word_similarity[node] = calculate_similarity(node, topic_words)
                    
                    # Print the results with combined URI format and individual nodes
                    #print(f"Node: {combined_node}")
                    
                    # Iterate through topics and print scores vertically
                    for topic_idx in range(len(topic_words)):
                        topic_name = f"Topic {topic_idx + 1}"
                        #print(f"  {topic_name}:")
                        tmp = 0
                        for node, word_scores in node_word_similarity.items():
                            score = word_scores.get(topic_name, {})
                            #print(f"    {node}: {score}")  # Print scores for each node under the topic
                            max_key = max(score, key = score.get)
                            max_val = score[max_key]
                            #print(max_val)
                            tmp += max_val
                        avg_tmp = tmp / len(node_word_similarity)
                        topic_avg.append(avg_tmp)
                    
                        #print(f"  Average Similarity for {topic_name}: {avg_tmp}\n")
                    
                    #print(f"Total Average for All Topics: {topic_avg}\n")
                    #for avg in topic_avg:
                    
                    #print(max(topic_avg))
                    if round(max(topic_avg),1) >= 0.5:
                        row['contextless_resource'] = 0
                        row['contextual_resouce'] = 1
                        row['contextless_comment'] = P
                        #print("contextual")
                        p_count = p_count + 1
                        contextual_P.append(f"{uris.strip()}\t {P}")
                    else:
                        row['contextless_resource'] = 1
                        row['contextual_resouce'] = 0
                        row['contextless_comment'] = AP
                        #print("contextless")
                        ap_count = ap_count + 1
                        contextless_AP.append(f"{uris.strip()}\t {AP}")
            
                    print("->", end=" ")
                
                json_string = json.dumps(row, ensure_ascii=False)
                file.write(json_string+"\n")
        return contextless_AP, contextual_P, p_count, ap_count
    




    def detect_non_hierarchical_nodes(self):
        P = "Hierarchical Nodes"
        AP = "Non-hierarchical Nodes"
        non_hierarchy_result_AP = []
        non_hierarchy_result_P = []
        p_count = 0
        ap_count = 0

        #for method, nodes, uri, doc in zip(self.http_method, self.processed_nodes, self.nodes, self.description):
        path = 'All-Data\Alldata.jsonl'
        with open(path, 'r+') as file:
            lines = file.read().strip().split("\n")
            file.seek(0)
            for line in lines:
                row = json.loads(line)
                if row["api_type"] == self.api_type and row["api_name"] == self.api_name:
                    uris = row['uri']  
                    #method = row['method']
                    #des = row['description']
                    nodes = self.clean.get_uri_nodes(uris)
                    #reliability = LexicalResult.Reliability()
                    result_information = ""
                    hierarchies = 0
                    good_type = True
                    P_detection = False
                    AP_detection = False

                    hier_matric = HierarchicalMetrics()

                    if len(nodes) >= 2:
                        for j in range(len(nodes) - 1):
                            nodeA = nodes[j]
                            nodeB = nodes[j + 1]

                            if nodeA and nodeB:
                                #print(f"{nodeA} ---- {nodeB}")
                                relation_type = hier_matric.reversed_hierarchy(nodeA, nodeB)

                                if relation_type:
                                    AP_detection = True
                                    result_information += f"Reversed hierarchy of type {relation_type} detected between {nodeA} and {nodeB}. "
                                    break

                                elif hier_matric.specialization_hierarchy(nodeA, nodeB):
                                    P_detection = True
                                    result_information += f"Specialization hierarchy detected between {nodeA} and {nodeB}. "
                                    hierarchies += 1
                                    #reliability.multiply_detection_reliability(LexicalResult.Reliability.AMBIGUOUS_DETECTION)

                        if P_detection or AP_detection:
                            max_chain_length = len(self.nodes) - 1
                            if AP_detection:
                                if hierarchies == 0:
                                    good_type = False
                                    result_information += f"{hierarchies} hierarchical relations were detected out of {max_chain_length}"
                            elif P_detection:
                                if hierarchies >= 1:
                                    good_type = True
                                    result_information += f"{hierarchies} hierarchical relations were detected out of {max_chain_length}"

                    if not good_type:
                        row['non_hierarchical_nodes'] = 1
                        row['hierarchical_nodes'] = 0
                        row['non_hierarchical_comment'] = AP
                        ap_count = ap_count + 1
                        non_hierarchy_result_AP.append(f"{uris.strip()}\t{AP}\t{result_information}")
                    
                    else:
                        row['non_hierarchical_nodes'] = 0
                        row['hierarchical_nodes'] = 1
                        row['non_hierarchical_comment'] = P
                        p_count = p_count + 1
                        non_hierarchy_result_P.append(f"{uris.strip()}\t{P}\t{result_information}")
                        
                    print("->", end=" ")
            
                json_string = json.dumps(row, ensure_ascii=False)
                file.write(json_string+"\n")
        return non_hierarchy_result_AP, non_hierarchy_result_P, p_count, ap_count
    


    def detect_less_cohesive_documentation(self):    
        P="Pertinent Documentation"
        AP="Non-pertinent Documentation"
        less_cohesive_AP = []
        less_cohesive_P = []
        p_count = 0
        ap_count = 0
        # Tokenize, remove stopwords, and lemmatize the descriptions
        nlp = spacy.load("en_core_web_lg")
        #stop_words = set(stopwords.words('english'))

        def preprocess_word(text):
            doc = nlp(text)
            tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
            return ' '.join(tokens)

        def similarity_calculator(word1, word2):
            word1 = nlp(preprocess_word(word1))
            word2 = nlp(preprocess_word(word2))
            simi = word1.similarity(word2)
            return simi

        def calculate_similarity(uri_node, topic_words):
            similarity_scores = {}
            for idx, word_list in enumerate(topic_words, start=1):
                word_similarity = {word: similarity_calculator(uri_node, word) for word in word_list}
                similarity_scores[f"Topic {idx}"] = word_similarity
            return similarity_scores

        #for method, combined_node, documentation, node_uri, des in zip(self.http_method, self.processed_nodes,self.processed_des, self.nodes, self.description):
            #print(f"\nn {method}---{combined_node}----{documentation}-{des}")
            # Calculate similarity for each individual node
        path = 'All-Data\Alldata.jsonl'
        with open(path, 'r+') as file:
            lines = file.read().strip().split("\n")
            file.seek(0)
            for line in lines:
                row = json.loads(line)
                if row["api_type"] == self.api_type and row["api_name"] == self.api_name:
                    uris = row['uri']  
                    #method = row['method']
                    des = row['description']
                    documentation = self.clean.preprocess_documentation(des)
                    combined_node = self.clean.get_uri_nodes(uris)
        
                    topics = len(combined_node)
                    #print(topics)
                    #print(combined_node)
                    #print(documentation)
                    if len(documentation)<1 or len(combined_node) < 1 :
                        p_count = p_count + 1
                        less_cohesive_P.append(f"-{uris.strip()}\t{P}\t{des}")
                        continue
                        
                    # Create a dictionary and corpus for LDA modeling
                    dictionary = corpora.Dictionary([documentation])
                    corpus = [dictionary.doc2bow(text) for text in [documentation]]

                    # Train LDA model
                    lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=topics, random_state=42)

                    # Get topic words from the model
                    topic_words = []
                    for topic_id in range(lda_model.num_topics):
                        topic_words.append([word for word, _ in lda_model.show_topic(topic_id)])
                    #print(topic_words)

                    # Display topic words horizontally
                    '''table = [["Topic " + str(i+1)] + words for i, words in enumerate(topic_words)]
                    print(tabulate(table, headers="firstrow", tablefmt="grid"))'''


                    node_word_similarity = {}
                    topic_avg = []
                    for node in combined_node:
                        node_word_similarity[node] = calculate_similarity(node, topic_words)
                        
                    
                    # Print the results with combined URI format and individual nodes
                    #print(f"Node: {combined_node}")
                    
                    # Iterate through topics and print scores vertically
                    for topic_idx in range(len(topic_words)):
                        topic_name = f"Topic {topic_idx + 1}"
                        #print(f"  {topic_name}:")
                        tmp = 0
                        for node, word_scores in node_word_similarity.items():
                            score = word_scores.get(topic_name, {})
                            #print(f"    {node}: {score}")  # Print scores for each node under the topic
                            #tmp1 = simi_average(score)
                            #print(tmp1)
                            max_value_key = max(score, key=score.get)
                            max_value = score[max_value_key]
                            #print(max_value)
                            tmp += max_value
                        avg_tmp = tmp / len(node_word_similarity)
                        topic_avg.append(avg_tmp)
                        #print(f"  Average Similarity for {topic_name}: {avg_tmp}\n")
                        
                    
                    #print(f"Total Average for All Topics: {topic_avg}\n")
                    #for avg in topic_avg:
                    #print(max(topic_avg))
                    if round(max(topic_avg), 1) >= 0.5:
                        row['less_cohesive_doc'] = 0
                        row['cohesive_doc'] = 1
                        row['less_cohesive_comment'] = P
                        #print("cohisive")
                        p_count = p_count + 1
                        less_cohesive_P.append(f"-{uris.strip()}\t{P}\t{des.strip()}")
                    else:
                        row['less_cohesive_doc'] = 1
                        row['cohesive_doc'] = 0
                        row['less_cohesive_comment'] = AP
                        #print("less_cohisive")
                        ap_count = ap_count + 1
                        less_cohesive_AP.append(f"-{uris.strip()}\t{AP}\t{des.strip()}")
                    print("->", end=" ")
                
                json_string = json.dumps(row, ensure_ascii=False)
                file.write(json_string+"\n")
                        
        return less_cohesive_AP, less_cohesive_P, p_count, ap_count
    


    def detect_inconsistent_documentations(self):
        post = ["return", "returns", "delete", "deletes", "update", "modify", "query", "list", "lists", "check", "checks", "verify", "get", "gets"]
        delete = ["get", "gets", "find", "finds", "search", "check", "list", "verify", "get", "gets"]
        put = ["delete", "deletes", "creates", "finds", "create", "find", "search", "checks", "lists", "check", "list"]
        get = ["delete", "deletes", "updates", "update", "creates", "create"]
        
        #description = []
        #nodes = []
        #http_method = []
        

        
        # Tokenize, remove stopwords, and lemmatize the descriptions
        nlp = spacy.load("en_core_web_lg")
        stop_words = set(stopwords.words('english'))

        def preprocess_data(text):
            tokens = word_tokenize(text.lower())
            tokens = [token for token in tokens if token.isalpha() and token not in stop_words]
            doc = nlp(" ".join(tokens))
            lemmatized_tokens = [f'{token}' for token in doc]
            return lemmatized_tokens

        P = "Consistent Documentation"
        AP = "Inconsistent Documentation"

        inconsistent_documentation_AP = []
        inconsistent_documentation_P = []
        p_count = 0
        ap_count = 0
        

        #for h_method, uri, documentation in zip(self.http_method, self.nodes, self.description):
        path = 'All-Data\Alldata.jsonl'
        with open(path, 'r+') as file:
            lines = file.read().strip().split("\n")
            file.seek(0)
            for line in lines:
                row = json.loads(line)
                if row["api_type"] == self.api_type and row["api_name"] == self.api_name:
                    uri = row['uri']  
                    h_method = row['method']
                    documentation = row['description']
                    #documentation = self.clean.preprocess_documentation(des)
                    #combined_node = self.clean.get_uri_nodes(uris)
        
                    method = h_method.lower().strip()
                    words = preprocess_data(documentation)
                    
                    
                    if method == "get":
                        if any(item in get for item in words):
                            row['inconsistent_doc'] = 1
                            row['consistent_doc'] = 0
                            row['inconsistent_comment'] = AP
                            inconsistent_documentation_AP.append(f"{h_method.strip()}\t{uri.strip()}\t{AP}\t{documentation.strip()}")
                            ap_count += 1
                        else:
                            row['inconsistent_doc'] = 0
                            row['consistent_doc'] = 1
                            row['inconsistent_comment'] = P
                            inconsistent_documentation_P.append(f"{h_method.strip()}\t{uri}\t{P.strip()}\t{documentation.strip()}")
                            p_count += 1
                    elif method == "delete":
                        if any(item in delete for item in words):
                            row['inconsistent_doc'] = 1
                            row['consistent_doc'] = 0
                            row['inconsistent_comment'] = AP
                            inconsistent_documentation_AP.append(f"{h_method.strip()}\t{uri.strip()}\t{AP}\t{documentation.strip()}")
                            ap_count += 1
                        else:
                            row['inconsistent_doc'] = 0
                            row['consistent_doc'] = 1
                            row['inconsistent_comment'] = P
                            inconsistent_documentation_P.append(f"{h_method.strip()}\t{uri.strip()}\t{P}\t{documentation.strip()}")
                            p_count += 1
                    elif method == "put":
                        if any(item in put for item in words):
                            row['inconsistent_doc'] = 1
                            row['consistent_doc'] = 0
                            row['inconsistent_comment'] = AP
                            inconsistent_documentation_AP.append(f"{h_method.strip()}\t{uri}\t{AP}\t{documentation.strip()}")
                            ap_count += 1
                        else:
                            row['inconsistent_doc'] = 0
                            row['consistent_doc'] = 1
                            row['inconsistent_comment'] = P
                            inconsistent_documentation_P.append(f"{h_method.strip()}\t{uri}\t{P}\t{documentation.strip()}")
                            p_count += 1
                    elif method == "post":
                        if any(item in post for item in words):
                            row['inconsistent_doc'] = 1
                            row['consistent_doc'] = 0
                            row['inconsistent_comment'] = AP
                            inconsistent_documentation_AP.append(f"{h_method.strip()}\t{uri}\t{AP}\t{documentation.strip()}")
                            ap_count += 1
                        else:
                            row['inconsistent_doc'] = 0
                            row['consistent_doc'] = 1
                            row['inconsistent_comment'] = P
                            inconsistent_documentation_P.append(f"{h_method.strip()}\t{uri}\t{P}\t{documentation.strip()}")
                            p_count += 1
                    else:
                        row['inconsistent_doc'] = 0
                        row['consistent_doc'] = 1
                        row['inconsistent_comment'] = P
                        inconsistent_documentation_P.append(f"{h_method.strip()}\t{uri.strip()}\t{P}\t{documentation.strip()}")
                        p_count += 1
                    print("->", end=" ")
                json_string = json.dumps(row, ensure_ascii=False)
                file.write(json_string+"\n")

        return inconsistent_documentation_AP, inconsistent_documentation_P, p_count, ap_count


    def detect_non_filtering_endpoint(self):
        P = "Filtering Endpoint"
        AP = "Non-Filtering Endpoint"

        non_filtering_endpoint_AP = []
        filtering_endpoint_P = []
        p_count = 0
        ap_count = 0
        
        def extract_intention(api_documentation):
            fetch_keywords = ["fetch", "return", "get", "retrieve", "list", "update", "delete"]
            update_keywords = ["update", "modify", "change", "edit"]
            create_keywords = ["create", "add", "post", "insert"]
            delete_keywords = ["delete", "remove", "destroy"]

            intention = ""
            api_doc_lower = api_documentation.lower()

            for word in fetch_keywords:
                if word in api_doc_lower:
                    intention = "Fetch"
                    break
            if not intention:
                for word in update_keywords:
                    if word in api_doc_lower:
                        intention = "Update"
                        break
            if not intention:
                for word in create_keywords:
                    if word in api_doc_lower:
                        intention = "Create"
                        break
            if not intention:
                for word in delete_keywords:
                    if word in api_doc_lower:
                        intention = "Delete"
                        break
            return intention
        
        path = 'All-Data\Alldata.jsonl'
        with open(path, 'r+') as file:
            lines = file.read().strip().split("\n")
            file.seek(0)
            for line in lines:
                row = json.loads(line)
                if row["api_type"] == self.api_type and row["api_name"] == self.api_name:
                    uri = row['uri']  
                    h_method = row['method']
                    documentation = row['description']
                    #documentation = self.clean.preprocess_documentation(des)
                    #combined_node = self.clean.get_uri_nodes(uris)
        
                    #method = h_method.lower().strip()
                    #words = preprocess_data(documentation)
        
        
                    # Extract intention from API documentation
                    Intention = extract_intention(documentation)

                    # Check if intention includes "Fetch" or "Return"
                    FetchIntention = "Fetch" in Intention or "Return" in Intention

                    # Check if parameter exists in request endpoint
                    has_param = '?' in uri or '{' in uri or '}' in uri or ':' in uri or '<' in uri or '>' in uri

                    # Determine endpoint type based on conditions
                    if (FetchIntention and not has_param) or (not FetchIntention and has_param):
                        row['non-filtering_endpoint'] = 1 
                        row['filtering_endpoint'] = 0
                        row['non-filtering_comment'] = AP
                        #return 'Non-Filtering Endpoint'  # Antipattern
                        non_filtering_endpoint_AP.append(f"{h_method.strip()}\t{uri}\t{AP}\t{documentation.strip()}")
                        ap_count += 1
                    elif (FetchIntention and has_param) or (not FetchIntention and not has_param):
                        #return 'Filtering Endpoint'  # Pattern
                        row['non-filtering_endpoint'] = 0 
                        row['filtering_endpoint'] = 1
                        row['non-filtering_comment'] = P
                        filtering_endpoint_P.append(f"{h_method.strip()}\t{uri}\t{P}\t{documentation.strip()}")
                        p_count += 1
                    print("->", end=" ")
                json_string = json.dumps(row, ensure_ascii=False)
                file.write(json_string+"\n")

        return non_filtering_endpoint_AP, filtering_endpoint_P, p_count, ap_count


    def detect_parameters_tunneling(self):
        P = "Parameter Adherence"
        AP = "Parameter Tunneling"

        parameter_tunneling_AP = []
        parameter_adherence_P = []
        p_count = 0
        ap_count = 0
        
        def extract_intention(api_documentation):
            fetch_keywords = ["fetch", "return", "get", "retrieve", "list"]
            update_keywords = ["update", "modify", "change", "edit"]
            create_keywords = ["create", "add", "post", "insert"]
            delete_keywords = ["delete", "remove", "destroy"]
            spf_keywords = ['sort', 'pagination', 'filter', 'paginate', 'filtering', 'rearrange']

            intention = ""
            api_doc_lower = api_documentation.lower()

            for word in fetch_keywords:
                if word in api_doc_lower:
                    intention = "Fetch"
                    break
            if not intention:
                for word in update_keywords:
                    if word in api_doc_lower:
                        intention = "Update"
                        break
            if not intention:
                for word in create_keywords:
                    if word in api_doc_lower:
                        intention = "Create"
                        break
            if not intention:
                for word in delete_keywords:
                    if word in api_doc_lower:
                        intention = "Delete"
                        break
            if not intention:
                for word in spf_keywords:
                    if word in api_doc_lower:
                        intention = 'spf'

            return intention
        
        path = 'All-Data\Alldata.jsonl'
        with open(path, 'r+') as file:
            lines = file.read().strip().split("\n")
            file.seek(0)
            for line in lines:
                row = json.loads(line)
                if row["api_type"] == self.api_type and row["api_name"] == self.api_name:
                    uri = row['uri']  
                    h_method = row['method']
                    documentation = row['description']
                    #documentation = self.clean.preprocess_documentation(des)
                    #combined_node = self.clean.get_uri_nodes(uris)
        
                    #method = h_method.lower().strip()
                    #words = preprocess_data(documentation)
        
        
                    intention = extract_intention(documentation)
                    query_param = '?' in uri
                    path_param = ('{' in uri and '}' in uri) or ('<' in uri and '>' in uri) or ':' in uri

                    sort_intention = False
                    identify_intention = False

                    if intention == "spf":
                        sort_intention = True
                    elif intention in ["Delete", "Update", "Fetch", "Delete", "Create"]:
                        identify_intention = True

                    if (query_param and sort_intention) or (path_param and identify_intention):
                        #return 'Parameter Adherence pattern'
                        row['parameter_tunneling'] = 0 
                        row['parameter_adherence'] = 1
                        row['parameter_tunneling_comment'] = P
                        parameter_adherence_P.append(f"{h_method.strip()}\t{uri}\t{P}\t{documentation.strip()}")
                        p_count += 1
                    elif (query_param and identify_intention) or (path_param and sort_intention):
                        row['parameter_tunneling'] = 1
                        row['parameter_adherence'] = 0
                        row['parameter_tunneling_comment'] = AP                        
                        parameter_tunneling_AP.append(f"{h_method.strip()}\t{uri}\t{AP}\t{documentation.strip()}")
                        ap_count += 1
                        #return 'Parameters Tunneling antipattern'
                    elif (intention and not (query_param or path_param)) or (not intention and (query_param or path_param)):
                        #return 'Parameters Tunneling antipattern'
                        row['parameter_tunneling'] = 1
                        row['parameter_adherence'] = 0
                        row['parameter_tunneling_comment'] = AP                        
                        parameter_tunneling_AP.append(f"{h_method.strip()}\t{uri}\t{AP}\t{documentation.strip()}")
                        ap_count += 1
                    else:
                        row['parameter_tunneling'] = 0
                        row['parameter_adherence'] = 1
                        row['parameter_tunneling_comment'] = 'Regular Endpoints'                        
                        parameter_adherence_P.append(f"{h_method.strip()}\t{uri}\t{P}\t{documentation.strip()}")
                        ap_count += 1
                    #return 'No specific pattern detected'
                    print("->", end=" ")
                json_string = json.dumps(row, ensure_ascii=False)
                file.write(json_string+"\n")

        return parameter_tunneling_AP, parameter_adherence_P, p_count, ap_count



    def detect_incosistent_resource_archetype(self):
        #import inflect
        #import re

        p = inflect.engine()
        def is_plural(noun):
            return p.singular_noun(noun) is not False
        def is_singular(noun):
            return not is_plural(noun)
        P = "Cosistent Resource Archetype"
        AP1 = "Singular Nouns Found in Consecutive Nodes"
        AP2 = "Plural Nouns Found in Consecutive Nodes"
        AP3 = "Controller is not a Verb"

        incosistent_resource_archetype_AP = []
        cosistent_resource_archetype_P = []
        p_count = 0
        ap_count = 0
        
        path = 'All-Data\Alldata.jsonl'
        with open(path, 'r+') as file:
            lines = file.read().strip().split("\n")
            file.seek(0)
            for line in lines:
                row = json.loads(line)
                if row["api_type"] == self.api_type and row["api_name"] == self.api_name:
                    uri = row['uri']  
                    h_method = row['method']
                    documentation = row['description']
                    #documentation = self.clean.preprocess_documentation(des)
                    #combined_node = self.clean.get_uri_nodes(uris)
        
                    #method = h_method.lower().strip()
                    #words = preprocess_data(documentation)

                    verbs = ["get", "post", "put", "delete", "update", "create", "fetch", "remove", "add", "edit", "patch"]
                    nodes = [node for node in uri.split('/') if node.isalpha()]

                    # Check for singular/plural pattern violations
                    for i in range(len(nodes) - 1):
                        if (not is_plural(nodes[i]) and not is_plural(nodes[i + 1])): # both singular
                            #return ['Inconsistent Resource Archetype Names antipattern', 'Violation: collection and store archetypes are not plural']
                            row['inconsistent_archetype'] = 1
                            row['consistent_archetype'] = 0
                            row['inconsistent_archetype_comment'] = AP1
                            incosistent_resource_archetype_AP.append(f"{h_method.strip()}\t{uri}\t{AP1}\t{documentation.strip()}")
                            ap_count += 1
                        if (is_plural(nodes[i]) and is_plural(nodes[i + 1])): # both plural
                            #return ['Inconsistent Resource Archetype Names antipattern', 'Document is not singular']
                            row['inconsistent_archetype'] = 1
                            row['consistent_archetype'] = 0
                            row['inconsistent_archetype_comment'] = AP2
                            incosistent_resource_archetype_AP.append(f"{h_method.strip()}\t{uri}\t{AP2}\t{documentation.strip()}")
                            ap_count += 1

                    # Analyze the last path segment for Controller
                    if len(nodes) > 2:
                        last_segment = nodes[-1]
                        first_word = re.split(r'[-_]', last_segment)[0]
                        if first_word[:-1].lower() in verbs:
                            if h_method.upper() not in ['GET', 'POST']:
                                #return ['Consistent Resource Archetype Names pattern', 'A controller action must be of type GET or POST']
                                row['inconsistent_archetype'] = 1
                                row['consistent_archetype'] = 0
                                row['inconsistent_archetype_comment'] = AP3
                                incosistent_resource_archetype_AP.append(f"{h_method.strip()}\t{uri}\t{AP3}\t{documentation.strip()}")
                                ap_count += 1
                            
                    if row['inconsistent_archetype'] != 1:
                        #return 'Consistent Resource Archetype'
                        row['inconsistent_archetype'] = 0
                        row['consistent_archetype'] = 1
                        row['inconsistent_archetype_comment'] = P
                        cosistent_resource_archetype_P.append(f"{h_method.strip()}\t{uri}\t{P}\t{documentation.strip()}")
                        p_count += 1
                    print("->", end=" ")
                json_string = json.dumps(row, ensure_ascii=False)
                file.write(json_string+"\n")

        return incosistent_resource_archetype_AP, cosistent_resource_archetype_P, p_count, ap_count
    
    def detect_identifier_ambiguity(self):
        P = "[Identifier is Enclosed in {} or <> or Starts with :]"
        P2 = "[Regular Endpoints]"
        AP = "[Identifier is Not Enclosed in {} or <> or does not Start with :]"

        identifier_ambiguity_AP = []
        identifier_annotation_P = []
        p_count = 0
        ap_count = 0
        
        path = 'All-Data\Alldata.jsonl'
        with open(path, 'r+') as file:
            lines = file.read().strip().split("\n")
            file.seek(0)
            for line in lines:
                row = json.loads(line)
                if row["api_type"] == self.api_type and row["api_name"] == self.api_name:
                    uri = row['uri']  
                    h_method = row['method']
                    documentation = row['description']
                    #documentation = self.clean.preprocess_documentation(des)
                    #combined_node = self.clean.get_uri_nodes(uris)
        
                    #method = h_method.lower().strip()
                    #words = preprocess_data(documentation)


                    parts = uri.split('/')
                    identifiers = [part for part in parts if part and not part.isdigit()]

                    for identifier in identifiers:
                        if (identifier.startswith("{") and identifier.endswith("}")) or (identifier.startswith("<") and identifier.endswith(">")) or identifier.startswith(":"):
                            #return "Identifier Annotation pattern"
                            row['identifier_ambiguity'] = 0
                            row['identifier_annotation'] = 1
                            row['identifier_ambiguity_comment'] = P
                            identifier_annotation_P.append(f"{h_method.strip()}\t{uri}\t{P}\t{documentation.strip()}")
                            p_count += 1

                    if row['identifier_annotation'] != 1:
                        if "{" in uri or "}" in uri or "<" in uri or ">" in uri or ":" in uri:
                            #return "Identifier Ambiguity antipattern" 
                            row['identifier_ambiguity'] = 1
                            row['identifier_annotation'] = 0
                            row['identifier_ambiguity_comment'] = AP
                            identifier_ambiguity_AP.append(f"{h_method.strip()}\t{uri}\t{AP}\t{documentation.strip()}")
                            ap_count += 1
                        else:
                            row['identifier_ambiguity'] = 0
                            row['identifier_annotation'] = 1
                            row['identifier_ambiguity_comment'] = P2
                            identifier_annotation_P.append(f"{h_method.strip()}\t{uri}\t{P2}\t{documentation.strip()}")
                            p_count += 1
                    print("->", end=" ")
                json_string = json.dumps(row, ensure_ascii=False)
                file.write(json_string+"\n")

        return identifier_ambiguity_AP, identifier_annotation_P, p_count, ap_count

    
    def detect_flat_endpoint(self):

        P = "Structed Endpoint"
        AP = "Complex Words Present in Endpoint"

        flat_endpoint_AP = []
        structed_endpoint_P = []
        p_count = 0
        ap_count = 0
        
        path = 'All-Data\Alldata.jsonl'
        with open(path, 'r+') as file:
            lines = file.read().strip().split("\n")
            file.seek(0)
            for line in lines:
                row = json.loads(line)
                if row["api_type"] == self.api_type and row["api_name"] == self.api_name:
                    uri = row['uri']  
                    h_method = row['method']
                    documentation = row['description']
                    #documentation = self.clean.preprocess_documentation(des)
                    #combined_node = self.clean.get_uri_nodes(uris)
        
                    #method = h_method.lower().strip()
                    #words = preprocess_data(documentation)

                    nodes = uri.split('/')
                    #print(nodes)
                    for node in nodes:
                        splitted_nodes = re.split(r'(?=[A-Z])|_', node)
                        #print(splitted_nodes)
                        if len(splitted_nodes) > 3:
                            #return "Flat Endpoint antipattern"
                            row['flat_endpoint'] = 1
                            row['structured_endpoint'] = 0
                            row['flat_endpoint_comment'] = AP
                            flat_endpoint_AP.append(f"{h_method.strip()}\t{uri}\t{AP}\t{documentation.strip()}")
                            ap_count += 1
                    if row['flat_endpoint'] != 1:
                        #return "Structured Endpoint pattern"
                        row['flat_endpoint'] = 0
                        row['structured_endpoint'] = 1
                        row['flat_endpoint_comment'] = P
                        structed_endpoint_P.append(f"{h_method.strip()}\t{uri}\t{P}\t{documentation.strip()}")
                        p_count += 1
                    print("->", end=" ")
                json_string = json.dumps(row, ensure_ascii=False)
                file.write(json_string+"\n")

        return flat_endpoint_AP, structed_endpoint_P, p_count, ap_count
