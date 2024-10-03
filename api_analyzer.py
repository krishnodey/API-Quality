from uri_cleaning import UriCleaning
#from hierarchical_metrics import HierarchicalMetrics
import re
#import nltk
from nltk.stem import WordNetLemmatizer #for pluralized nodes
from nltk.corpus import wordnet as wn #for nondescritive URI
#nltk.download('wordnet')  # Download WordNet data if not downloaded
#nltk.download('stopwords')
#nltk.download('punkt')
#import gensim
from gensim import corpora
from gensim.models import LdaModel
#from gensim.models.coherencemodel import CoherenceModel
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import spacy
#from collections import defaultdict
#from itertools import combinations
from sklearn.metrics.pairwise import cosine_similarity
from tabulate import tabulate
import warnings
#import math
#import csv
import json
import inflect 
import os

    

class ApiAnalyzer:
    def __init__(self, api_type, api):
        #self.URI = URI
        self.api_type = api_type
        self.api_name = api
        warnings.filterwarnings("ignore", category=UserWarning)
        self.http_verb = []
        self.uris = []
        self.descriptions = []
        self.parameters = []
        self.processed_des =[]
        self.processed_nodes =[]
        

        
        self.clean = UriCleaning()


        input_file = f"{api_type}-APIs\{api}\{api}.txt"
        process_file = f"{api_type}-APIs\{api}\Processed_{api}.txt"

        if os.path.exists(process_file):
            print("opening process file")
            with open(process_file, "r") as file:
                lines = file.read().strip().split("\n")
                #print(lines)
                for line in lines:
                    row = json.loads(line)
                    #print(row['http_verb'])
                    self.http_verb.append(row['http_verb'])
                    self.uris.append(row['uri'])
                    self.processed_nodes.append(row['processed_uri'])
                    self.descriptions.append(row['description'])
                    self.parameters.append(row['parameter'])
                    self.processed_des.append(row['processed_des_para'])
        else:     
            with open(input_file, "r") as file, open(process_file, "w") as pro_file:
                for line in file:
                    #print(line)
                    line  = line.split(">>")
                    if len(line) == 4:
                        verb, uri, des, para = line[0].strip(), line[1].strip(), line[2].strip(), line[3].strip()
                    else:
                        verb, uri, des, para = line[0].strip(), line[1].strip(), line[2].strip(), ''

                    self.http_verb.append(verb.strip())
                    self.uris.append(uri.strip())
                    self.descriptions.append(des.strip())
                    self.parameters.append(para.strip())

                    pro_nodes = self.clean.get_uri_nodes(uri.strip())
                    pro_des = self.clean.preprocess_documentation(f"{des.strip()} {para.strip()}")
                    self.processed_nodes.append(pro_nodes)
                    self.processed_des.append(pro_des)

                    line_dict = {"http_verb": verb.strip(), "uri": uri.strip(), "processed_uri" : pro_nodes, "description": des.strip(), "parameter": para.strip(), "processed_des_para": pro_des}
                    json_string=json.dumps(line_dict,ensure_ascii=False)
                    pro_file.write(json_string+"\n")        
                
        



    def detect_amorphous_uri(self):
        found_AP = 0
    
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
        
        path = f"All-Data\\temp\\{self.api_type}\\{self.api_name}.jsonl"
        with open(path, 'w') as file:
            i = 1
            for verb, uri, des, para in zip(self.http_verb, self.uris, self.descriptions, self.parameters):
                row = {"id": i,"api_type": self.api_type, "api_name": self.api_name,"http_verb": verb, "uri": uri, "descriptions": des, "parameters": para}
                words = uri.strip().split("/")
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
                        elif uri.strip()[-1] == '/' or uri.strip()[-1] == '\\':
                            found_AP = 1
                            comment += " [trailing slash found] "
                            flag = 1
                        else:
                            for extension in extensions:
                                if extension.lower() in uri.lower() or extension.upper() in uri:
                                    found_AP = 1
                                    comment += " [extension found] "
                                    flag = 1
                    if flag == 1:
                        break
                if found_AP == 1:
                    row.update({"amorphous_uri": 1, "tidy_uri": 0, 'amorphous_comment': comment})
                else:
                    comment = "Tidy Endpoint"
                    row.update({"amorphous_uri": 0, "tidy_uri": 1, 'amorphous_comment': comment})
                print("->", end=" ")
                i = i +1

                json_string=json.dumps(row, ensure_ascii=False)
                file.write(json_string+"\n")     
    




    def detect_non_standard_uri(self):
        P = "Standard End-point"
        AP = "Non-standard End-point"
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

        
        path = f"All-Data\\temp\\{self.api_type}\\{self.api_name}.jsonl"
        with open(path, 'r+') as file:
            lines = file.read().strip().split("\n")
            file.seek(0)
            file.truncate()  # Clear the file content

            for uri, line in zip(self.uris, lines):
                row = json.loads(line)

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
                    row.update({"non_standard_uri": 1, "standard_uri": 0, "non_standard_comment": comment})
                else:
                    comment = "Standard Endpoint"
                    row.update({"non_standard_uri": 0, "standard_uri": 1, "non_standard_comment": comment})
                print("->", end=" ")
            
                json_string=json.dumps(row, ensure_ascii=False)
                file.write(json_string+"\n") 
    
    

    def detect_crudy_uri(self):
        P = "Verbless End-point"
        AP = "CRUDy End-point"
        crudyWords = ["create", "make", "write", "read", "search", "show", "take", "delete", "destroy", "cancel", "remove", "update", "copy", "move", "upgrade", "notify"]

        path = f"All-Data\\temp\\{self.api_type}\\{self.api_name}.jsonl"
        with open(path, 'r+') as file:
            lines = file.read().strip().split("\n")
            file.seek(0)
            file.truncate()
            for line, nodes in zip(lines, self.processed_nodes):
                row = json.loads(line)

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
                    row.update({"crudy_uri": 1, "verbless_uri": 0, "crudy_comment": comment})
                else:
                    row.update({"crudy_uri": 0, "verbless_uri": 1, "crudy_comment": comment})
                print("->", end=" ")
        
                json_string=json.dumps(row, ensure_ascii=False)
                file.write(json_string+"\n")
    
    

    def detect_unversioned_uris(self):
        path = f"All-Data\\temp\\{self.api_type}\\{self.api_name}.jsonl"
        with open(path, 'r+') as file:
            lines = file.read().strip().split("\n")
            file.seek(0)
            for line, uri in zip(lines, self.uris):
                row = json.loads(line)
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
                matches = any(re.match(regex, uri) for regex in regex_list)

                if matches:
                    comment = "Version Found"
                    row.update({"unversioned_uri": 0, "versioned_uri": 1, "unversioned_comment": comment})
                else:
                    
                    comment = "No Version Found"
                    row.update({"unversioned_uri": 1, "versioned_uri": 0, "unversioned_comment": comment})
                    
                #row['unversioned_comment'] = comment
                print("->", end=" ")
                json_string = json.dumps(row, ensure_ascii=False)
                file.write(json_string+"\n")
                


    def detect_pluralized_node(self):
        P = "Singularized Nodes"
        AP = "Pluralized Nodes"
    
        def is_plural(word):
            lemmatizer = WordNetLemmatizer()
            lemma = lemmatizer.lemmatize(word, pos='n')
            return word != lemma
        #print(is_plural("sources"))

        #for method, uris, nodes, doc in zip(self.http_method, self.nodes, self.processed_nodes, self.description):
        path = f"All-Data\\temp\\{self.api_type}\\{self.api_name}.jsonl"
        with open(path, 'r+') as file:
            lines = file.read().strip().split("\n")
            file.seek(0)
            for line, method, nodes in zip(lines, self.http_verb, self.processed_nodes):
                row = json.loads(line)
                comment1 = "Singular last node with POST method"
                comment2 = "Pluralized last node with POST method"
                comment3 = "Pluralized last node with PUT and DELETE method"
                comment4 = "Singular last node with PUT and DELETE method"
                comment5 = "Regular methods"

                if len(nodes) < 1:
                    row.update({"pluralized_nodes": 0, "singularized_nodes": 1, "pluralized_comment": comment5})
                    continue
                last_node = nodes[-1]

                if method.strip() == "POST":
                    if is_plural(last_node):
                        row.update({"pluralized_nodes": 0, "singularized_nodes": 1, "pluralized_comment": comment2})
                    else:
                        row.update({"pluralized_nodes": 1, "singularized_nodes": 0, "pluralized_comment": comment1})
                        

                elif method.strip() == "DELETE" or method.strip() == "PUT":
                    if is_plural(last_node):
                        row.update({"pluralized_nodes": 1, "singularized_nodes": 0, "pluralized_comment": comment3})
                    else:
                        row.update({"pluralized_nodes": 0, "singularized_nodes": 1, "pluralized_comment": comment4})
                else:
                    row.update({"pluralized_nodes": 0, "singularized_nodes": 1, "pluralized_comment": comment5})  
                    
                print("->", end=" ")
                
                json_string = json.dumps(row, ensure_ascii=False)
                file.write(json_string+"\n")
 
    

    def detect_non_descriptive_uri(self):
        P = "Self-descriptive End-point"
        AP = "Non-descriptive End-point"
    
        path = f"All-Data\\temp\\{self.api_type}\\{self.api_name}.jsonl"
        with open(path, 'r+') as file:
            lines = file.read().strip().split("\n")
            file.seek(0)
            for line, uris, nodes in zip(lines, self.uris, self.processed_nodes):
                row = json.loads(line)
        
                pattern = True

                for word in nodes:
                    # Perform word lookup operation
                    synsets = wn.synsets(word.strip())
                    
                    if synsets:
                        pattern = pattern | True
                    else:
                        pattern = pattern & False

                if not pattern:
                    row.update({"non_descriptive_uri" : 1, "descriptive_uri": 0, "non_descriptive_comment": AP})
                elif pattern:
                    row.update({"non_descriptive_uri" : 0, "descriptive_uri": 1, "non_descriptive_comment": P})                   
                print("->", end=" ")
                json_string = json.dumps(row, ensure_ascii=False)
                file.write(json_string+"\n")
    

    def detect_contextless(self):
        
        P = "Contextual Resource Names"
        AP = "Contextless Resource Names"
        
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

       
        path = f"All-Data\\temp\\{self.api_type}\\{self.api_name}.jsonl"
        with open(path, 'r+') as file:
            lines = file.read().strip().split("\n")
            file.seek(0)
            for line, uris, combined_node in zip(lines, self.uris, self.processed_nodes):
                row = json.loads(line)
        
                if len(combined_node) < 1:
                    row.update({"contextless_resource": 0, "contextual_resouce": 1, "contextless_comment": P})
                    
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
                    #print("contextual")
                    row.update({"contextless_resource": 0, "contextual_resouce": 1, "contextless_comment": P})
                else:
                    row.update({"contextless_resource": 1, "contextual_resouce": 0, "contextless_comment": AP})
        
                print("->", end=" ")
            
                json_string = json.dumps(row, ensure_ascii=False)
                file.write(json_string+"\n")
       
    




    def detect_non_hierarchical_nodes(self):
        
        def specialization_hierarchy(word1, word2):  # top_down_relationship
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

        def reversed_hierarchy(word1, word2):  # down_top_relationship
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

        P = "Hierarchical Nodes"
        AP = "Non-hierarchical Nodes"

        path = f"All-Data\\temp\\{self.api_type}\\{self.api_name}.jsonl"
        with open(path, 'r+') as file:
            lines = file.read().strip().split("\n")
            file.seek(0)
            for line, uris, nodes in zip(lines, self.uris, self.processed_nodes):
                row = json.loads(line)
                
                result_information = ""
                hierarchies = 0
                good_type = True
                P_detection = False
                AP_detection = False


                if len(nodes) >= 2:
                    for j in range(len(nodes) - 1):
                        nodeA = nodes[j]
                        nodeB = nodes[j + 1]

                        if nodeA and nodeB:
                            #print(f"{nodeA} ---- {nodeB}")
                            relation_type = reversed_hierarchy(nodeA, nodeB)

                            if relation_type:
                                AP_detection = True
                                result_information += f"Reversed hierarchy of type {relation_type} detected between {nodeA} and {nodeB}. "
                                break

                            elif specialization_hierarchy(nodeA, nodeB):
                                P_detection = True
                                result_information += f"Specialization hierarchy detected between {nodeA} and {nodeB}. "
                                hierarchies += 1
                                #reliability.multiply_detection_reliability(LexicalResult.Reliability.AMBIGUOUS_DETECTION)

                    if P_detection or AP_detection:
                        max_chain_length = len(nodes) - 1
                        if AP_detection:
                            if hierarchies == 0:
                                good_type = False
                                #result_information += f"{hierarchies} hierarchical relations were detected out of {max_chain_length}"
                        elif P_detection:
                            if hierarchies >= 1:
                                good_type = True
                                #result_information += f"{hierarchies} hierarchical relations were detected out of {max_chain_length}"

                if not good_type:
                    row.update({"non_hierarchical_nodes" : 1, "hierarchical_nodes": 0, "non_hierarchical_comment": AP})
                
                else:
                    row.update({"non_hierarchical_nodes" : 0, "hierarchical_nodes": 1, "non_hierarchical_comment": P})
                    
                print("->", end=" ")
        
                json_string = json.dumps(row, ensure_ascii=False)
                file.write(json_string+"\n")
    


    def detect_less_cohesive_documentation(self):    
        P="Pertinent Documentation"
        AP="Non-pertinent Documentation"
        
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

        
        path = f"All-Data\\temp\\{self.api_type}\\{self.api_name}.jsonl"
        with open(path, 'r+') as file:
            lines = file.read().strip().split("\n")
            file.seek(0)
            for line, uris, des, combined_node, documentation in zip(lines, self.uris, self.descriptions, self.processed_nodes, self.processed_des):
                row = json.loads(line)
        
                topics = len(combined_node)
                #print(topics)
                #print(combined_node)
                #print(documentation)
                if len(documentation)<1 or len(combined_node) < 1 :
                    row.update({"less_cohesive_doc": 0, "cohesive_doc": 1, "less_cohesive_comment": AP})
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
                    row.update({"less_cohesive_doc": 0, "cohesive_doc": 1, "less_cohesive_comment": P})
                    #print("cohisive")
                else:
                    row.update({"less_cohesive_doc": 1, "cohesive_doc": 0, "less_cohesive_comment": AP})
                    #print("less_cohisive")
                print("->", end=" ")
            
                json_string = json.dumps(row, ensure_ascii=False)
                file.write(json_string+"\n")
                        
    


    def detect_inconsistent_documentations(self):
        post = ["return", "returns", "delete", "deletes", "update", "modify", "query", "list", "lists", "check", "checks", "verify", "get", "gets"]
        delete = ["get", "gets", "find", "finds", "search", "check", "list", "verify", "get", "gets"]
        put = ["delete", "deletes", "creates", "finds", "create", "find", "search", "checks", "lists", "check", "list"]
        get = ["delete", "deletes", "updates", "update", "creates", "create"]
        
        # Tokenize, remove stopwords, and lemmatize the descriptions
        #nlp = spacy.load("en_core_web_lg")
        #stop_words = set(stopwords.words('english'))

        # def preprocess_data(text):
        #     tokens = word_tokenize(text.lower())
        #     tokens = [token for token in tokens if token.isalpha() and token not in stop_words]
        #     doc = nlp(" ".join(tokens))
        #     lemmatized_tokens = [f'{token}' for token in doc]
        #     return lemmatized_tokens

        P = "Consistent Documentation"
        AP = "Inconsistent Documentation"

        path = f"All-Data\\temp\\{self.api_type}\\{self.api_name}.jsonl"
        with open(path, 'r+') as file:
            lines = file.read().strip().split("\n")
            file.seek(0)
            for line, h_method,  words in zip(lines, self.http_verb, self.processed_des):
                row = json.loads(line)
        
                method = h_method.lower().strip()
                #words = preprocess_data(documentation)
                if method == "get":
                    if any(item in get for item in words):
                        # row['inconsistent_doc'] = 1
                        # row['consistent_doc'] = 0
                        # row['inconsistent_comment'] = AP
                        row.update({"inconsistent_doc": 1, "consistent_doc": 0, "inconsistent_comment": AP})
                    else:
                        # row['inconsistent_doc'] = 0
                        # row['consistent_doc'] = 1
                        # row['inconsistent_comment'] = P
                        row.update({"inconsistent_doc": 0, "consistent_doc": 1, "inconsistent_comment": P})
                elif method == "delete":
                    if any(item in delete for item in words):
                        row.update({"inconsistent_doc": 1, "consistent_doc": 0, "inconsistent_comment": AP})
                    else:
                        # row['inconsistent_doc'] = 0
                        # row['consistent_doc'] = 1
                        # row['inconsistent_comment'] = P
                        row.update({"inconsistent_doc": 0, "consistent_doc": 1, "inconsistent_comment": P})
                elif method == "put":
                    if any(item in put for item in words):
                        # row['inconsistent_doc'] = 1
                        # row['consistent_doc'] = 0
                        # row['inconsistent_comment'] = AP
                        row.update({"inconsistent_doc": 1, "consistent_doc": 0, "inconsistent_comment": AP})
                    else:
                        # row['inconsistent_doc'] = 0
                        # row['consistent_doc'] = 1
                        # row['inconsistent_comment'] = P
                        row.update({"inconsistent_doc": 0, "consistent_doc": 1, "inconsistent_comment": P})
                elif method == "post":
                    if any(item in post for item in words):
                        # row['inconsistent_doc'] = 1
                        # row['consistent_doc'] = 0
                        # row['inconsistent_comment'] = AP
                        row.update({"inconsistent_doc": 1, "consistent_doc": 0, "inconsistent_comment": AP})
                    else:
                        # row['inconsistent_doc'] = 0
                        # row['consistent_doc'] = 1
                        # row['inconsistent_comment'] = P
                        row.update({"inconsistent_doc": 0, "consistent_doc": 1, "inconsistent_comment": P})
                else:
                    # row['inconsistent_doc'] = 0
                    # row['consistent_doc'] = 1
                    # row['inconsistent_comment'] = P
                    row.update({"inconsistent_doc": 0, "consistent_doc": 1, "inconsistent_comment": P})
                   
                print("->", end=" ")
                json_string = json.dumps(row, ensure_ascii=False)
                file.write(json_string+"\n")



    # def detect_non_filtering_endpoint(self):
    #     P = "Filtering Endpoint"
    #     AP = "Non-Filtering Endpoint"

    #     non_filtering_endpoint_AP = []
    #     filtering_endpoint_P = []
    #     p_count = 0
    #     ap_count = 0
        
    #     def extract_intention(api_documentation):
    #         fetch_keywords = [""]
    #         update_keywords = ["update", "modify", "change", "edit"]
    #         create_keywords = ["create", "add", "post", "insert"]
    #         delete_keywords = ["delete", "remove", "destroy"]

    #         intention = ""
    #         api_doc_lower = api_documentation.lower()

    #         for word in fetch_keywords:
    #             if word in api_doc_lower:
    #                 intention = "Fetch"
    #                 break
    #         if not intention:
    #             for word in update_keywords:
    #                 if word in api_doc_lower:
    #                     intention = "Update"
    #                     break
    #         if not intention:
    #             for word in create_keywords:
    #                 if word in api_doc_lower:
    #                     intention = "Create"
    #                     break
    #         if not intention:
    #             for word in delete_keywords:
    #                 if word in api_doc_lower:
    #                     intention = "Delete"
    #                     break
    #         return intention
        
    #     path = f"All-Data\\temp\\{self.api_type}\\{self.api_name}.jsonl"
    #     with open(path, 'r+') as file:
    #         lines = file.read().strip().split("\n")
    #         file.seek(0)
    #         file.truncate()
    #         for line, method, uri, documentation in zip(lines, self.http_verb, self.uris, self.descriptions+self.parameters):
    #             row = json.loads(line)
    
    #             # Extract intention from API documentation
    #             Intention = extract_intention(documentation)

    #             # Check if intention includes "Fetch" or "Return"
    #             FetchIntention = "Fetch" in Intention or "Return" in Intention

    #             # Check if parameter exists in request endpoint
    #             has_param = '?' in uri or '{' in uri or '}' in uri or ':' in uri or '<' in uri or '>' in uri

    #             # Determine endpoint type based on conditions
    #             if (FetchIntention and not has_param) or (not FetchIntention and has_param):
    #                 row.update({"non-filtering_endpoint": 1, "filtering_endpoint": 0, "non-filtering_comment": AP})
    #                 #return 'Non-Filtering Endpoint'  # Antipattern
    #                 non_filtering_endpoint_AP.append(f"{method.strip()}\t{uri}\t{AP}\t{documentation.strip()}")
    #                 ap_count += 1
    #             elif (FetchIntention and has_param) or (not FetchIntention and not has_param):
    #                 #return 'Filtering Endpoint'  # Pattern
    #                 row.update({"non-filtering_endpoint": 0, "filtering_endpoint": 1, "non-filtering_comment": P})
    #                 filtering_endpoint_P.append(f"{method.strip()}\t{uri}\t{P}\t{documentation.strip()}")
    #                 p_count += 1
    #             print("->", end=" ")
    #             json_string = json.dumps(row, ensure_ascii=False)
    #             file.write(json_string+"\n")

    #     return non_filtering_endpoint_AP, filtering_endpoint_P, p_count, ap_count


    def detect_parameters_tunneling(self):
        P = "Parameter Adherence"
        AP = "Parameter Tunneling"
        path = f"All-Data\\temp\\{self.api_type}\\{self.api_name}.jsonl"
        with open(path, 'r+') as file:
            lines = file.read().strip().split("\n")
            file.seek(0)
            file.truncate()
            for line, method, uri in zip(lines, self.http_verb, self.uris):
                row = json.loads(line)
                query_param = '?' in uri
                path_param = ('{' in uri and '}' in uri) or ('<' in uri and '>' in uri) or ':' in uri

                if (query_param and method.strip().upper() != 'GET'):
                    row.update({"parameter_tunneling": 1, "parameter_adherence": 0, "parameter_tunneling_comment": AP})
                elif (path_param and method.strip().upper() in ['POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS', 'CONNECT', 'TRACE']):
                    row.update({"parameter_tunneling": 0, "parameter_adherence": 1, "parameter_tunneling_comment": P})                
                else:
                    comm = 'Regular Endpoints' 
                    row.update({"parameter_tunneling": 0, "parameter_adherence": 1, "parameter_tunneling_comment": comm})                       
                    
                print("->", end=" ")
                json_string = json.dumps(row, ensure_ascii=False)
                file.write(json_string+"\n")



    def detect_incosistent_resource_archetype(self):
        #import inflect
        #import re

        p = inflect.engine()
        def is_plural(noun):
            return p.singular_noun(noun) is not False
        # def is_singular(noun):
        #     return not is_plural(noun)
        P = "Cosistent Resource Archetype"
        AP1 = "Singular Nouns Found in Consecutive Nodes"
        AP2 = "Plural Nouns Found in Consecutive Nodes"
        AP3 = "Controller is not a Verb"

        def split_uri(uri):
            extensions = [".json", ".html", ".pdf", ".txt", ".xml", ".jpg", ".jpeg", ".png", ".gif", ".csv", ".htm", ".zip", ".v1", ".v2", ".v3"]
            pattern = re.compile('|'.join([re.escape(ext) for ext in extensions]))
            uri = pattern.sub('', uri)
            
            # Remove parts enclosed in {}, <>, followed by :, and parts after ?
            cleaned_uri = re.sub(r'\{.*?\}|\<.*?\>|:[^/]*|\?.*', '', uri)
            
            # Split the URI by slashes
            parts = cleaned_uri.strip().split('/')
            
            clean_nodes = []
            for part in parts:
                if part:  # Skip empty parts
                    # Remove unwanted characters (digits, $, %, ., etc.)
                    part = re.sub(r'[^a-zA-Z_-]', '', part)  # Keep letters, _, and -
                    
                    # Split by underscore, hyphen, or camelCase
                    last_part = re.split(r'_|-|(?<!^)(?=[A-Z])', part)
                    
                    # Add the last part if there are multiple segments
                    if len(last_part) > 1:
                        clean_nodes.append(last_part[-1].lower())
                    elif part:  # Ensure part is not empty after cleaning
                        clean_nodes.append(part.lower())  # Add the part as-is if no split is needed
                    if "api" in clean_nodes:
                        clean_nodes.remove("api")
            
            return clean_nodes

        
        path = f"All-Data\\temp\\{self.api_type}\\{self.api_name}.jsonl"
        with open(path, 'r+') as file:
            lines = file.read().strip().split("\n")
            file.seek(0)
            file.truncate()
            for line, method, uri, documentation, clean_nodes in zip(lines, self.http_verb, self.uris, self.descriptions+self.parameters, self.processed_nodes):
                row = json.loads(line)

                
                #nodes = [node for node in uri.split('/') if node.isalpha()]
                print(uri)
                print(clean_nodes)
                
                nodes = split_uri(uri)
                print(nodes)
                if len(nodes) <= 2:
                     row.update({"inconsistent_archetype": 0, "consistent_archetype": 1, "inconsistent_archetype_comment": "Less than 3 nodes present in endpoint"})
                else:
                    flag = 0
                    # Check for singular/plural pattern violations
                    for i in range(len(nodes) - 1):
                        if (not is_plural(nodes[i]) and not is_plural(nodes[i + 1])): # both singular
                            #return ['Inconsistent Resource Archetype Names antipattern', 'Violation: collection and store archetypes are not plural']
                            flag = 1
                            row.update({"inconsistent_archetype": 1, "consistent_archetype": 0, "inconsistent_archetype_comment": AP1})
                        if (is_plural(nodes[i]) and is_plural(nodes[i + 1])): # both plural
                            #return ['Inconsistent Resource Archetype Names antipattern', 'Document is not singular'
                            flag = 1
                            row.update({"inconsistent_archetype": 1, "consistent_archetype": 0, "inconsistent_archetype_comment": AP2})
                            

                    # Analyze the last path segment for Controller
                    verbs = ["get", "post", "put", "delete", "update", "create", "fetch", "remove", "add", "edit", "patch"]
                    if len(nodes) > 2:
                        last_segment = uri.split('/')[-1]
                        # print(last_segment)
                        first_word = re.split(r'_|-|(?<!^)(?=[A-Z])', last_segment)[0]
                        #print(first_word)
                        if (first_word.lower() in verbs):
                            # print(method.upper())
                            if (method.upper().strip() == "POST"):
                                flag = 1
                                row.update({"inconsistent_archetype": 0, "consistent_archetype": 1, "inconsistent_archetype_comment": "Controller used with get or post"})
                            else:
                                # print('wrong brunch')
                                flag = 1
                                row.update({"inconsistent_archetype": 1, "consistent_archetype": 0, "inconsistent_archetype_comment": "Controller is not used with get or post"})
                    if flag != 1:
                        row.update({"inconsistent_archetype": 0, "consistent_archetype": 1, "inconsistent_archetype_comment": "Consistent Arhetypes"})
                        
                print("->", end=" ")
                #print(f"{row['inconsistent_archetype']} ---- {row['consistent_archetype']}")
                json_string = json.dumps(row, ensure_ascii=False)
                file.write(json_string+"\n")

    
    def detect_identifier_ambiguity(self):
        P = "[Identifier is Enclosed in {} or <> or Starts with :]"
        P2 = "[Regular Endpoints]"
        AP = "[Identifier is Not Enclosed in {} or <> or does not Start with :]"
        
        path = f"All-Data\\temp\\{self.api_type}\\{self.api_name}.jsonl"
        with open(path, 'r+') as file:
            lines = file.read().strip().split("\n")
            file.seek(0)
            file.truncate()
            for line, uri in zip(lines, self.uris):
                row = json.loads(line)

                #parts = uri.split('/')
                #identifiers = [part for part in parts if part and not part.isdigit()]
                #identifiers = [subpart for part in parts.split('/') if part and not part.isdigit() for subpart in part.split('.')]
                uri = uri.strip()
                identifiers = [subpart for part in uri.split('/') if part and not part.isdigit() for subpart in re.split(r'[.?]', part)]
                # print(identifiers)
                flag = 0
                for identifier in identifiers:
                    identifier = identifier.strip()
                    if (identifier.startswith("{") and identifier.endswith("}")) or (identifier.startswith("<") and identifier.endswith(">")) or identifier.startswith(":"):
                        #return "Identifier Annotation pattern"
                        #print(True)
                        flag = 1
                        row.update({"identifier_ambiguity": 0, "identifier_annotation": 1, "identifier_ambiguity_comment": P})

                if flag != 1:
                    if "_Id" in uri.lower() or "_ID" in uri :# or {" in uri or "}" in uri or "<" in uri or ">" in uri or ":" in uri:
                        #return "Identifier Ambiguity antipattern"
                        row.update({"identifier_ambiguity": 1, "identifier_annotation": 0, "identifier_ambiguity_comment": AP})
                    else:
                        row.update({"identifier_ambiguity": 0, "identifier_annotation": 1, "identifier_ambiguity_comment": P2})
                        
                print("->", end=" ")
                json_string = json.dumps(row, ensure_ascii=False)
                file.write(json_string+"\n")

 

    
    def detect_flat_endpoint(self):

        P = "Structed Endpoint"
        AP = "Complex Words Present in Endpoint"
        path = f"All-Data\\temp\\{self.api_type}\\{self.api_name}.jsonl"
        with open(path, 'r+') as file:
            lines = file.read().strip().split("\n")
            file.seek(0)
            file.truncate()
            for line, uri in zip(lines, self.uris):
                row = json.loads(line)

                flag = 0
                uri = uri.split('?')[0]
                nodes = uri.split('/')
                #print(nodes)
                for node in nodes:
                    splitted_nodes = re.split(r'(?=[A-Z])|_|-', node)
                    # print(splitted_nodes)
                    if len(splitted_nodes) > 4:
                        #return "Flat Endpoint antipattern"
                        flag = 1
                        row.update({"flat_endpoint": 1, "structured_endpoint": 0, "flat_endpoint_comment": AP})
                if flag == 0:
                    #return "Structured Endpoint pattern"
                    row.update({"flat_endpoint": 0, "structured_endpoint": 1, "flat_endpoint_comment": P})
                print("->", end=" ")
                json_string = json.dumps(row, ensure_ascii=False)
                file.write(json_string+"\n")

  
