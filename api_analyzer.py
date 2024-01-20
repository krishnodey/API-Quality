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
    

class ApiAnalyzer:
    def __init__(self, URI):
        self.URI = URI

    def detect_amorphous_uri(self, URI=None):
        URI = URI if URI else self.URI
        P = "Tidy End-point"
        AP = "Amorphous End-point"
        found_AP = 0
        p_count = 0
        ap_count = 0
        amorphus_result_AP = []
        amorphus_result_P = []
        extensions = [".json", ".html", ".pdf", ".txt", ".xml", ".jpg", ".jpeg", ".png", ".gif", ".csv", ".htm", ".zip"]

        for line in URI:
            comment = ""
            found_AP = 0

            if "%5F".lower() in line.lower() or "%5F" in line:
                found_AP = 1
                comment += " [underscore found] "

            c = line.strip()[-1]
            if c == '/' or c == '\\':
                found_AP = 1
                comment += " [trailing slash found] "

            for extension in extensions:
                if extension.lower() in line.lower() or extension.upper() in line:
                    found_AP = 1
                    comment += " [extension found] "

            if found_AP == 1:
                ap_count = ap_count + 1
                amorphus_result_AP.append(line.strip() + "\t" + AP + "\t" + comment)
            else:
                p_count = p_count + 1
                amorphus_result_P.append(line.strip() + "\t" + P + "\t" + comment)

        return amorphus_result_AP, amorphus_result_P, p_count, ap_count
    
    def detect_non_standard_uri(self, URI=None):
        URI = URI if URI else self.URI
        P = "Standard End-point"
        AP = "Non-standard End-point"
        standard_uri_result_AP = []
        standard_uri_result_P = []
        p_count = 0
        ap_count = 0

        for line in URI:
            comment = ""
            found_AP = 0

            if any(c in line.lower() for c in ['�', '�', '�']):
                found_AP = 1
                comment += " [sw spec char found] "

            if any(c in line.lower() for c in ['�', '�', '�', '�', '�', '�', '�', '�', '�', '�', '�', '�']):
                found_AP = 1
                comment += " [fr spec char found] "

            if ' ' in line or '\t' in line:
                found_AP = 1
                comment += " [black space/tab found] "

            if '--' in line:
                found_AP = 1
                comment += " [double hyphens found] "

            if any(c in line.lower() for c in ['!', '@', '#', '$', '~', '^', '*', '>', '<']):
                found_AP = 1
                comment += " [unknown char found] "

            if found_AP == 1:
                standard_uri_result_AP.append(f"{line.strip()}\t{AP}\t{comment}")
                ap_count += 1
            else:
                standard_uri_result_P.append(f"{line.strip()}\t{P}\t{comment}")
                p_count += 1

        return standard_uri_result_AP, standard_uri_result_P, p_count, ap_count
    
    

    def detect_crudy_uri(self, URI=None):
        URI = URI if URI else self.URI
        P = "Verbless End-point"
        AP = "CRUDy End-point"
        crudyWords = ["create", "make", "write", "read", "search", "show", "take", "delete", "destroy", "cancel", "remove", "update", "copy", "move", "upgrade", "notify"]
        crudyURIResult_AP = []
        crudyURIResult_P = []
        p_count = 0
        ap_count = 0

        for line in self.URI:
            good_type = False
            comment = ""
            ap_found = False

            # Preprocessing: Splitting and cleaning the nodes
            nodes = re.split(r'/', line.strip())
            nodes = [re.sub(r'[^a-zA-Z0-9]', '', node) for node in nodes]

            splitted_nodes = []
            for node in nodes:
                #tmp = re.split(r'(?<!(^|[A-Z]))(?=[A-Z])|(?<!^)(?=[A-Z][a-z])', node)
                words = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', node)

                splitted_nodes.extend(words)

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
                ap_count = ap_count + 1
                crudyURIResult_AP.append(f"{line.strip()}\t{AP}\t{comment}")
            else:
                p_count = p_count + 1
                crudyURIResult_P.append(f"{line.strip()}\t{P}\t{comment}")

        return crudyURIResult_AP, crudyURIResult_P, p_count, ap_count
    
    

    def detect_unversioned_uris(self, URI=None):
        URI = URI if URI else self.URI
        versioned_result_P = []
        unversioned_result_AP = []
        p_count = 0
        ap_count = 0

        for line in self.URI:
            regex_list = [
                ".*v1.*", ".*v0.*", ".*v2.*", ".*v3.*", ".*v3.*",
                ".*/v/.*", ".*api-version=.*"
            ]

            matches = any(re.match(regex, line) for regex in regex_list)

            if matches:
                versioned_result_P.append(f"{line.strip()} [Version found.]")
                p_count += 1
            else:
                unversioned_result_AP.append(f"{line.strip()} [No version found.]")
                ap_count += 1

        return unversioned_result_AP, versioned_result_P , p_count, ap_count


    def detect_pluralized_node(self, URI=None):
        URI = URI if URI else self.URI
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

        for line in URI:
            tmp = line.split(">>")
            http_method = tmp[0].strip()
            nodes = [st.strip().replace("[^a-zA-Z0-9]", "") for st in tmp[1].split("/")]
            splitted_nodes = []
            for node in nodes:
                tmp1 = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', node)
                splitted_nodes.extend(tmp1)
            last_node = splitted_nodes[-1]

            comment1 = " [Singular last node with POST method.] "
            comment2 = " [Pluralized last node with POST method.] "
            comment3 = " [Pluralized last node with PUT|DELETE method.] "
            comment4 = " [Singular last node with PUT|DELETE method.] "

            if http_method == "POST":
                if is_plural(last_node):
                    p_count += 1
                    pluralised_result_P.append(f"{tmp[0]}\t{tmp[1].strip()}\t{P}\t{comment2}")
                else:
                    ap_count += 1
                    pluralised_result_AP.append(f"{tmp[0]}\t{tmp[1].strip()}\t{AP}\t{comment1}")

            elif http_method == "DELETE" or http_method == "PUT":
                if is_plural(last_node):
                    ap_count += 1
                    pluralised_result_AP.append(f"{tmp[0]}\t{tmp[1].strip()}\t{AP}\t{comment3}")
                else:
                    p_count += 1
                    pluralised_result_P.append(f"{tmp[0]}\t{tmp[1].strip()}\t{P}\t{comment4}")
            else:
                p_count += 1
                pluralised_result_P.append(f"{tmp[0]}\t{tmp[1].strip()}\t regular methods.")

        return pluralised_result_AP, pluralised_result_P, p_count, ap_count
    

    def detect_non_descriptive_uri(self, URI=None):
        URI = URI if URI else self.URI
        non_descriptive_AP = []
        self_descriptive_P = []
        P = "Self-descriptive End-point"
        AP = "Non-descriptive End-point"
        p_count = 0
        ap_count = 0

        for line in URI:
            #uri_nodes = uri.split("/")
            #print(uri_nodes)
            #nodes = [st.strip().replace("[^a-zA-Z0-9]", "") for st in line.split("/")]
            #print(nodes)
            clean = UriCleaning()
            splitted_nodes = clean.get_uri_nodes(line)
            #print(splitted_nodes)
            '''splitted_nodes = []
            for node in nodes:
                tmp1 = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', node)
                splitted_nodes.extend(tmp1)
            print(splitted_nodes)'''
        
            pattern = True

            for word in splitted_nodes:
                # Perform word lookup operation equivalent to Java's Dictionary.getInstance().lookupAllIndexWords(word)
                synsets = wn.synsets(word.strip())
                
                if synsets:
                    pattern = pattern | True
                else:
                    pattern = pattern & False

            if not pattern:
                ap_count = ap_count + 1
                non_descriptive_AP.append(f"{line.strip()}\t {AP}")
            elif pattern:
                p_count = p_count + 1
                self_descriptive_P.append(f"{line.strip()}\t {P}")

        return non_descriptive_AP, self_descriptive_P, p_count, ap_count
    

    def detect_contextless(self, URI=None):
        URI = URI if URI else self.URI
        contextless_AP = []
        contextual_P = []
        P = "Contextual Resource Names"
        AP = "Contextless Resource Names"
        p_count = 0
        ap_count = 0
        #print(lines)
        description = []
        nodes = []
        for ln in URI:
            tmp = ln.split(">>")

            if len(ln) == 4:
                text = f"{tmp[2]} {tmp[3]}"
                description.append(text)
            description.append(tmp[2])
            nodes.append(tmp[1])
        #print(description)
        #print(nodes)


        # Tokenize, remove stopwords, and lemmatize the descriptions
        nlp = spacy.load("en_core_web_lg")
        stop_words = set(stopwords.words('english'))

        def preprocess_data(text):
            tokens = word_tokenize(text.lower())
            tokens = [token for token in tokens if token.isalpha() and token not in stop_words]
            doc = nlp(" ".join(tokens))
            lemmatized_tokens = [token.lemma_ for token in doc]
            return lemmatized_tokens


        def preprocess_word(text):
            doc = nlp(text)
            tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
            return ' '.join(tokens)

        def similarity_calculator(word1, word2):
            word1 = nlp(preprocess_word(word1))
            word2 = nlp(preprocess_word(word2))
            simi = word1.similarity(word2)
            return simi

        def simi_average(data):
            if isinstance(data, dict):
                values = list(data.values())  
                average = sum(values) / len(values) if len(values) > 0 else 0  # Calculate average
                return average
            else:
                return data  # Return the input value as it is if not a dictionary
        
        clean = UriCleaning()
        #splitted_nodes = clean.get_uri_nodes(line)

        processed_des =[]
        for des in description:
            processed_des.append(preprocess_data(des))
        processed_nodes =[]
        for nd in nodes:
            processed_nodes.append(clean.get_uri_nodes(nd))

        # Create a dictionary and corpus for LDA modeling
        dictionary = corpora.Dictionary(processed_des)
        corpus = [dictionary.doc2bow(text) for text in processed_des]

        # Train LDA model
        lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=5, random_state=42)

        # Get topic words from the model
        topic_words = []
        for topic_id in range(lda_model.num_topics):
            topic_words.append([word for word, _ in lda_model.show_topic(topic_id)])
        #print(topic_words)

        '''# Display topic words horizontally
        table = [["Topic " + str(i+1)] + words for i, words in enumerate(topic_words)]
        print(tabulate(table, headers="firstrow", tablefmt="grid"))'''

        def calculate_similarity(uri_node, topic_words):
            similarity_scores = {}
            for idx, word_list in enumerate(topic_words, start=1):
                word_similarity = {word: similarity_calculator(uri_node, word) for word in word_list}
                similarity_scores[f"Topic {idx}"] = word_similarity
            return similarity_scores

        for combined_node, origianl_node in zip(processed_nodes, nodes):
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
                    tmp1 = simi_average(score)
                    #print(tmp1)
                    tmp += tmp1
                avg_tmp = tmp / len(node_word_similarity)
                topic_avg.append(avg_tmp)
                #print(f"  Average Similarity for {topic_name}: {avg_tmp}\n")
            
            #print(f"Total Average for All Topics: {topic_avg}\n")
            #for avg in topic_avg:
            #print(max(topic_avg))
            if max(topic_avg) > 0.3:
                #print("contextual")
                p_count = p_count + 1
                contextual_P.append(f"{origianl_node}\t {P}")
            else:
                #print("contextless")
                ap_count = ap_count + 1
                contextless_AP.append(f"{origianl_node}\t {AP}")

        return contextless_AP, contextual_P, p_count, ap_count
    




    def detect_non_hierarchical_nodes(self, URI=None):
        URI = URI if URI else self.URI
        P = "Hierarchical Nodes"
        AP = "Non-hierarchical Nodes"
        non_hierarchy_result_AP = []
        non_hierarchy_result_P = []
        p_count = 0
        ap_count = 0

        for uri in URI:
            #print(uri)
            clean = UriCleaning()
            nodes = clean.get_uri_nodes(uri)
            #print(nodes)

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
                    max_chain_length = len(nodes) - 1
                    if AP_detection:
                        if hierarchies == 0:
                            good_type = False
                            result_information += f"{hierarchies} hierarchical relations were detected out of {max_chain_length}"
                    elif P_detection:
                        if hierarchies >= 1:
                            good_type = True
                            result_information += f"{hierarchies} hierarchical relations were detected out of {max_chain_length}"

            if not good_type:
                ap_count = ap_count + 1
                non_hierarchy_result_AP.append(f"{uri}\t{AP}\t{result_information}")
            else:
                p_count = p_count + 1
                non_hierarchy_result_P.append(f"{uri}\t{P}\t{result_information}")
        return non_hierarchy_result_AP, non_hierarchy_result_P, p_count, ap_count
    

    

    '''def detect_less_cohesive_documentation(Self, URI):

        description = []
        nodes = []
        for ln in URI:
            tmp = ln.split(">>")
            description.append(tmp[2])
            nodes.append(tmp[1])
        #print(description)
        #print(nodes)
            
        P="Pertinent vs. Documentation"
        AP="Non-pertinent Documentation"
        less_cohesive_AP = []
        less_cohesive_P = []
        p_count = 0
        ap_count = 0
        obj = LessCohesive()

        for uri, documentation in zip(nodes, description):
            
            result = obj.less_cohesive_documentation_analysis(uri, documentation)
            
            if result == 1:
                ap_count = ap_count + 1
                less_cohesive_AP.append(f"{nodes}\t{AP}\t{documentation}")
            elif result == 0:
                p_count = p_count + 1
                less_cohesive_P.append(f"{nodes}\t{P}\t{documentation}")

        return less_cohesive_AP, less_cohesive_P, p_count, ap_count'''
    


    def detect_less_cohesive_documentation(self, URI):    
        description = []
        nodes = []
        for ln in URI:
            tmp = ln.split(">>")
            if len(ln) == 4:
                text = f"{tmp[2]} {tmp[3]}"
                description.append(text)
            description.append(tmp[2])
            nodes.append(tmp[1])
        #print(description)
        #print(nodes)
            
        P="Pertinent Documentation"
        AP="Non-pertinent Documentation"
        less_cohesive_AP = []
        less_cohesive_P = []
        p_count = 0
        ap_count = 0

        # Tokenize, remove stopwords, and lemmatize the descriptions
        nlp = spacy.load("en_core_web_lg")
        stop_words = set(stopwords.words('english'))

        def preprocess_data(text):
            tokens = word_tokenize(text.lower())
            tokens = [token for token in tokens if token.isalpha() and token not in stop_words]
            doc = nlp(" ".join(tokens))
            lemmatized_tokens = [token.lemma_ for token in doc]
            return lemmatized_tokens


        def preprocess_word(text):
            doc = nlp(text)
            tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
            return ' '.join(tokens)

        def similarity_calculator(word1, word2):
            word1 = nlp(preprocess_word(word1))
            word2 = nlp(preprocess_word(word2))
            simi = word1.similarity(word2)
            return simi

        def simi_average(data):
            if isinstance(data, dict):
                values = list(data.values())  
                average = sum(values) / len(values) if len(values) > 0 else 0  # Calculate average
                return average
            else:
                return data  # Return the input value as it is if not a dictionary
        
        clean = UriCleaning()
        #splitted_nodes = clean.get_uri_nodes(line)
        
        processed_des =[]
        for des in description:
            processed_des.append(preprocess_data(des))
        processed_nodes =[]
        for nd in nodes:
            processed_nodes.append(clean.get_uri_nodes(nd))
        #print(processed_des)
        #print(processed_nodes)

        for new in processed_nodes:
            for i in range(len(new)):
                val = clean.set_Acronym(new[i])
                if val is not None:
                    for index in range(len(val)):
                        if i + index < len(new):
                            new[i + index] = val[index]
                        else:
                            new.append(val[index])
        #print(processed_nodes)
        
        def calculate_similarity(uri_node, topic_words):
            similarity_scores = {}
            for idx, word_list in enumerate(topic_words, start=1):
                word_similarity = {word: similarity_calculator(uri_node, word) for word in word_list}
                similarity_scores[f"Topic {idx}"] = word_similarity
            return similarity_scores

        for combined_node, documentation, node_uri, des in zip(processed_nodes,processed_des, nodes, description):
            # Calculate similarity for each individual node
            topics = len(combined_node)
            #print(topics)
            #print(combined_node)
            
            #print(documentation)
            if len(documentation)<1:
                p_count = p_count + 1
                less_cohesive_AP.append(f"-{node_uri}\t{AP}\t{des}")
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
                    tmp1 = simi_average(score)
                    #print(tmp1)
                    tmp += tmp1
                avg_tmp = tmp / len(node_word_similarity)
                topic_avg.append(avg_tmp)
                #print(f"  Average Similarity for {topic_name}: {avg_tmp}\n")
            
            #print(f"Total Average for All Topics: {topic_avg}\n")
            #for avg in topic_avg:
            #print(max(topic_avg))
            if max(topic_avg) > 0.3:
                #print("cohisive")
                p_count = p_count + 1
                less_cohesive_P.append(f"-{node_uri.strip()}\t{P}\t{des.strip()}")
            else:
                #print("less_cohisive")
                ap_count = ap_count + 1
                less_cohesive_AP.append(f"-{node_uri.strip()}\t{AP}\t{des.strip()}")
        return less_cohesive_AP, less_cohesive_P, p_count, ap_count
    


    def detect_inconsistent_documentations(self, URI=None):
        URI = URI if URI else self.URI

        post = ["return", "returns", "delete", "deletes", "update", "modify", "query", "list", "lists", "check", "checks", "verify", "get", "gets"]
        delete = ["get", "gets", "find", "finds", "search", "check", "list", "verify", "get", "gets"]
        put = ["delete", "deletes", "creates", "finds", "create", "find", "search", "checks", "lists", "check", "list"]
        get = ["delete", "deletes", "updates", "update", "creates", "create"]
        
        description = []
        nodes = []
        http_method = []
        for ln in URI:
            tmp = ln.split(">>")
            if len(ln) == 4:
                text = f"{tmp[2]} {tmp[3]}"
                description.append(text)
            description.append(tmp[2])
            nodes.append(tmp[1])
            http_method.append(tmp[0])
            #print(description)
            #print(nodes)
            #print(http_method)

        # Tokenize, remove stopwords, and lemmatize the descriptions
        nlp = spacy.load("en_core_web_lg")
        stop_words = set(stopwords.words('english'))

        def preprocess_data(text):
            tokens = word_tokenize(text.lower())
            tokens = [token for token in tokens if token.isalpha() and token not in stop_words]
            doc = nlp(" ".join(tokens))
            lemmatized_tokens = [token.lemma_ for token in doc]
            return lemmatized_tokens

        P = "Consistent Documentation"
        AP = "Inconsistent Documentation"

        inconsistent_documentation_AP = []
        inconsistent_documentation_P = []
        p_count = 0
        ap_count = 0
        
        clean = UriCleaning()

        for method, uri, documentation in zip(http_method, nodes, description):
            #documentation = documentation.strip()
            method = method.lower().strip()
            print(method)
            words = preprocess_data(documentation)
            print(words)
            #uri = clean.get_uri_nodes(node)
            #print(words)
            #print(uri)
            
            if method in "get":
                #if any(item in get for item in words):

                if any(item in get for item in words):
                    inconsistent_documentation_AP.append(f"{method.strip()}\t{uri.strip()}\t{AP}\t{documentation.strip()}")
                    ap_count += 1
                else:
                    inconsistent_documentation_P.append(f"{method.strip()}\t{uri}\t{P.strip()}\t{documentation.strip()}")
                    p_count += 1

            elif method in "delete":
                if any(item in delete for item in words):
                    inconsistent_documentation_AP.append(f"{method.strip()}\t{uri.strip()}\t{AP}\t{documentation.strip()}")
                    ap_count += 1
                else:
                    inconsistent_documentation_P.append(f"{method.strip()}\t{uri.strip()}\t{P}\t{documentation.strip()}")
                    p_count += 1

            elif method in "put":
                if any(item in put for item in words):
                    inconsistent_documentation_AP.append(f"{method.strip()}\t{uri}\t{AP}\t{documentation.strip()}")
                    ap_count += 1
                else:
                    inconsistent_documentation_P.append(f"{method.strip()}\t{uri}\t{P}\t{documentation.strip()}")
                    p_count += 1

            elif method in "post":
                if any(item in post for item in words):
                    inconsistent_documentation_AP.append(f"{method.strip()}\t{uri}\t{AP}\t{documentation.strip()}")
                    ap_count += 1
                else:
                    inconsistent_documentation_P.append(f"{method.strip()}\t{uri}\t{P}\t{documentation.strip()}")
                    p_count += 1

            else:
                inconsistent_documentation_P.append(f"{method.strip()}\t{uri.strip()}\t{P}\t{documentation.strip()}")
                p_count += 1

        return inconsistent_documentation_AP, inconsistent_documentation_P, p_count, ap_count



    

