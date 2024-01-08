from uri_cleaning import UriCleaning
import re
import nltk
from nltk.stem import WordNetLemmatizer #for pluralized nodes
from nltk.corpus import wordnet as wn #for nondescritive URI
nltk.download('wordnet')  # Download WordNet data if not downloaded

    

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
            print(splitted_nodes)
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


