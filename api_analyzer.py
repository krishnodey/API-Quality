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
import math
    

class ApiAnalyzer:
    def __init__(self, URI):
        self.URI = URI
        warnings.filterwarnings("ignore", category=UserWarning)


    def detect_amorphous_uri(self, URI=None):
        URI = URI if URI else self.URI
        

        P = "Tidy End-point"
        AP = "Amorphous End-point"
        found_AP = 0
        p_count = 0
        ap_count = 0
        amorphus_result_AP = []
        amorphus_result_P = []
        amp_lst = []
        str = 'HTTP-Method\tURI\tDescription\tAnti-Pattern\tPattern\tComment'
        amp_lst.append(str)
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
        
        for line in URI:
            tmp = line.split(">>")
            #print(tmp[1])
            words = tmp[1].strip().split("/")
            if len(tmp) == 4:
                tmp[3] = ' '.join(tmp[3].split())
                tmp[2] = f"{tmp[2].strip()}{tmp[3].strip()}"
            #print(tmp[2].split("/n"))


            #print(words)
            comment = ""
            found_AP = 0

            if "%5F".lower() in tmp[1].lower() or "%5F" in tmp[1]:
                found_AP = 1
                comment += " [underscore found] "
                #c = line.strip()[-1]
            elif tmp[1].strip()[-1] == '/' or tmp[1].strip()[-1] == '\\':
                found_AP = 1
                comment += " [trailing slash found] "
            else:
                for extension in extensions:
                    if extension.lower() in tmp[1].lower() or extension.upper() in tmp[1]:
                        found_AP = 1
                        comment += " [extension found] "
            
            #elif any(ch.isupper() for wd in words):
            for word in words:
                word = word.strip()
                word = word.replace("<", '').replace(">", '') #replace("{", '').replace("}",'')
                if word: 
                    if word[0].strip() == "{" and word[-1].strip() == "}":
                        #print("variable")
                        continue
                    elif any(ch.isupper() for ch in word) and is_camel_case(word) == "False":
                        found_AP = 1
                        comment += " [uppercase found] "

            if found_AP == 1:
                ap_count = ap_count + 1
                amorphus_result_AP.append(tmp[1].strip() + "\t" + AP + "\t" + comment)
                str = f"{tmp[0].strip()} \t {tmp[1].strip()} \t {tmp[2].strip()} \t 1 \t 0 \t{comment}"
            else:
                p_count = p_count + 1
                amorphus_result_P.append(tmp[1].strip() + "\t" + P + "\t" + comment)
                str = f"{tmp[0].strip()} \t {tmp[1].strip()} \t {tmp[2].strip()} \t 0 \t 1 \t{comment}"
            amp_lst.append(str)
            

        return amorphus_result_AP, amorphus_result_P, p_count, ap_count, amp_lst
    
    def detect_non_standard_uri(self, URI=None):
        URI = URI if URI else self.URI
        P = "Standard End-point"
        AP = "Non-standard End-point"
        standard_uri_result_AP = []
        standard_uri_result_P = []
        standard_lst = []
        str = 'HTTP-Method\tURI\tDescription\tAnti-Pattern\tPattern\tComment'
        standard_lst.append(str)
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



        for ur in URI:
            tmp = ur.strip().split(">>")
            #print(tmp)
            line = tmp[1].strip()
            if len(tmp) == 4:
                tmp[3] = ' '.join(tmp[3].split())
                tmp[2] = f"{tmp[2]}{tmp[3]}"

            #print(tmp[1])
            #words = tmp[1].strip().split("/")
            #print(words)
            #print(words)

            
            comment = ""
            found_AP = 0
            line = line.strip()

            
            if any(c in line.lower() for c in european_languages):
                found_AP = 1
                comment += " [european char found] "
            elif any(c in line.lower() for c in cyrillic_languages):
                found_AP = 1
                comment += " [ cyrillic char found] "
            elif any(c in line.lower() for c in greek_language):
                found_AP = 1
                comment += " [ greek char found] "
            elif any(c in line.lower() for c in arabic_language):
                found_AP = 1
                comment += " [ arabic char found] "
            elif any(c in line.lower() for c in japanese_language):
                found_AP = 1
                comment += " [ japanese char found] "
            elif ' ' in line.strip() or '\t' in line.strip():
                found_AP = 1
                comment += " [blank space/tab found] "
            elif '--' in line:
                found_AP = 1
                comment += " [double hyphens found] "
            elif any(c in line.lower() for c in ['!', '@', '#', '$', '~', '^', '*', '>', '<']):
                found_AP = 1
                comment += " [unknown char found] "

            if found_AP == 1:
                str = f"{tmp[0].strip()} \t {tmp[1].strip()} \t {tmp[2].strip()} \t 1 \t 0 \t{comment}"
                standard_uri_result_AP.append(f"{line.strip()}\t{AP}\t{comment}")
                ap_count += 1
            else:
                str = f"{tmp[0].strip()} \t {tmp[1].strip()} \t {tmp[2].strip()} \t 0 \t 1 \t{comment}"
                standard_uri_result_P.append(f"{line.strip()}\t{P}\t{comment}")
                p_count += 1
            standard_lst.append(str)

        return standard_uri_result_AP, standard_uri_result_P, p_count, ap_count, standard_lst
    
    

    def detect_crudy_uri(self, URI=None):
        URI = URI if URI else self.URI
        P = "Verbless End-point"
        AP = "CRUDy End-point"
        crudyWords = ["create", "make", "write", "read", "search", "show", "take", "delete", "destroy", "cancel", "remove", "update", "copy", "move", "upgrade", "notify"]
        crudyURIResult_AP = []
        crudyURIResult_P = []
        p_count = 0
        ap_count = 0
        crudy_lst = []
        str = 'HTTP-Method\tURI\tDescription\tAnti-Pattern\tPattern\tComment'
        crudy_lst.append(str)
        for ur in URI:
            tmp = ur.strip().split(">>")
            #print(tmp)
            line = tmp[1].strip()

            if len(tmp) == 4:
                tmp[3] = ' '.join(tmp[3].split())
                tmp[2] = f"{tmp[2]}{tmp[3]}"


            #print(line)
            good_type = False
            comment = ""
            ap_found = False

            # Preprocessing: Splitting and cleaning the nodes
            '''nodes = re.split(r'/', line.strip())
            nodes = [re.sub(r'[^a-zA-Z0-9]', '', node) for node in nodes]
            print(nodes)
            splitted_nodes = []
            for node in nodes:
                #tmp = re.split(r'(?<!(^|[A-Z]))(?=[A-Z])|(?<!^)(?=[A-Z][a-z])', node)
                words = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', node)

                splitted_nodes.extend(words)
            print(splitted_nodes)'''
            
            clean = UriCleaning()
            nodes = clean.get_uri_nodes(line)
            #print(nodes)
            #for new in nodes:
            for i in range(len(nodes)):
                val = clean.set_Acronym(nodes[i])
                if val is not None:
                    for index in range(len(val)):
                        if i + index < len(nodes):
                            nodes[i + index] = val[index]
                        else:
                            nodes.append(val[index])
            #print(processed_nodes)
                            
            #print(nodes)

            
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
                str = f"{tmp[0].strip()} \t {tmp[1].strip()} \t {tmp[2].strip()} \t 1 \t 0 \t{comment}"
                ap_count = ap_count + 1
                crudyURIResult_AP.append(f"{line.strip()}\t{AP}\t{comment}")
            else:
                str = f"{tmp[0].strip()} \t {tmp[1].strip()} \t {tmp[2].strip()} \t 0 \t 1 \t{comment}"
                p_count = p_count + 1
                crudyURIResult_P.append(f"{line.strip()}\t{P}\t{comment}")
            crudy_lst.append(str)
        return crudyURIResult_AP, crudyURIResult_P, p_count, ap_count, crudy_lst
    
    

    def detect_unversioned_uris(self, URI=None):
        URI = URI if URI else self.URI
        versioned_result_P = []
        unversioned_result_AP = []
        p_count = 0
        ap_count = 0
        version_lst = []
        str = 'HTTP-Method\tURI\tDescription\tAnti-Pattern\tPattern\tComment'
        version_lst.append(str)
        #print(URI)

        for ur in URI:
            tmp = ur.strip().split(">>")
            #print(tmp)
            line = tmp[1].strip()
            if len(tmp) == 4:
                tmp[3] = ' '.join(tmp[3].split())
                tmp[2] = f"{tmp[2]}{tmp[3]}"



            '''regex_list = [
                ".*v1.*", ".*v0.*", ".*v2.*", ".*v3.*", ".*v3.*",
                ".*/v/.*", ".*api-version=.*", "/v\d+\.\d+/", "/v\d+\.\d+/"
            ]'''
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


            matches = any(re.match(regex, line) for regex in regex_list)

            if matches:
                str = f"{tmp[0].strip()} \t {tmp[1].strip()} \t {tmp[2].strip()} \t 0 \t 1 \t Version Found"
                versioned_result_P.append(f"{line.strip()} \t Version Found")
                p_count += 1
            else:
                str = f"{tmp[0].strip()} \t {tmp[1].strip()} \t {tmp[2].strip()} \t 1 \t 0 \t No Version Found"
                unversioned_result_AP.append(f"{line.strip()} \t No Version Found")
                ap_count += 1
            version_lst.append(str)

        return unversioned_result_AP, versioned_result_P , p_count, ap_count, version_lst


    def detect_pluralized_node(self, URI=None):
        URI = URI if URI else self.URI
        pluralised_result_AP = []
        pluralised_result_P = []
        P = "Singularized Nodes"
        AP = "Pluralized Nodes"
        p_count = 0
        ap_count = 0
        plural_lst = []
        str = 'HTTP-Method\tURI\tDescription\tAnti-Pattern\tPattern\tComment'
        plural_lst.append(str)

        def is_plural(word):
            lemmatizer = WordNetLemmatizer()
            lemma = lemmatizer.lemmatize(word, pos='n')
            return word != lemma
        #print(is_plural("sources"))

        for line in URI:
            tmp = line.split(">>")
            #print(tmp[1])
            http_method = tmp[0].strip()

            if len(tmp) == 4:
                tmp[3] = ' '.join(tmp[3].split())
                tmp[2] = f"{tmp[2]}{tmp[3]}"


            '''nodes = [st.strip().replace("[^a-zA-Z0-9]", "") for st in tmp[1].split("/")]
            splitted_nodes = []
            for node in nodes:
                tmp1 = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', node)
                splitted_nodes.extend(tmp1)
            print(splitted_nodes)
            last_node = splitted_nodes[-1]
            print(last_node)'''

            clean = UriCleaning()
            nodes = clean.get_uri_nodes(tmp[1].strip())

            
            #for new in nodes:
            for i in range(len(nodes)):
                val = clean.set_Acronym(nodes[i])
                if val is not None:
                    for index in range(len(val)):
                        if i + index < len(nodes):
                            nodes[i + index] = val[index]
                        else:
                            nodes.append(val[index])
            #print(processed_nodes)

            #print(nodes)
            #print(last_node)

            comment1 = " [Singular last node with POST method.] "
            comment2 = " [Pluralized last node with POST method.] "
            comment3 = " [Pluralized last node with PUT|DELETE method.] "
            comment4 = " [Singular last node with PUT|DELETE method.] "
            comment5 = "Regular methods"

            #if no nodes in uri
            if len(nodes) < 1: 
                p_count += 1
                pluralised_result_P.append(f"{tmp[0]}\t{tmp[1].strip()}\t{P}\t {comment5}")
                str = f"{tmp[0].strip()} \t {tmp[1].strip()} \t {tmp[2].strip()} \t 0 \t 1 \t {comment5}"
                continue
            last_node = nodes[-1]

            if http_method == "POST":
                if is_plural(last_node):
                    p_count += 1
                    pluralised_result_P.append(f"{tmp[0]}\t{tmp[1].strip()}\t{P}\t{comment2}")
                    str = f"{tmp[0].strip()} \t {tmp[1].strip()} \t {tmp[2].strip()} \t 0 \t 1 \t {comment2}"
                else:
                    ap_count += 1
                    pluralised_result_AP.append(f"{tmp[0]}\t{tmp[1].strip()}\t{AP}\t{comment1}")
                    str = f"{tmp[0].strip()} \t {tmp[1].strip()} \t {tmp[2].strip()} \t 1 \t 0 \t {comment1}"

            elif http_method == "DELETE" or http_method == "PUT":
                if is_plural(last_node):
                    ap_count += 1
                    pluralised_result_AP.append(f"{tmp[0]}\t{tmp[1].strip()}\t{AP}\t{comment3}")
                    str = f"{tmp[0].strip()} \t {tmp[1].strip()} \t {tmp[2].strip()} \t 1 \t 0 \t {comment3}"
                else:
                    p_count += 1
                    pluralised_result_P.append(f"{tmp[0]}\t{tmp[1].strip()}\t{P}\t{comment4}")
                    str = f"{tmp[0].strip()} \t {tmp[1].strip()} \t {tmp[2].strip()} \t 0 \t 1 \t {comment4}"
            else:
                p_count += 1
                pluralised_result_P.append(f"{tmp[0]}\t{tmp[1].strip()}\t {comment5}")
                str = f"{tmp[0].strip()} \t {tmp[1].strip()} \t {tmp[2].strip()} \t 0 \t 1 \t {comment5}"
            plural_lst.append(str)
        return pluralised_result_AP, pluralised_result_P, p_count, ap_count, plural_lst
    

    def detect_non_descriptive_uri(self, URI=None):
        URI = URI if URI else self.URI
        non_descriptive_AP = []
        self_descriptive_P = []
        P = "Self-descriptive End-point"
        AP = "Non-descriptive End-point"
        p_count = 0
        ap_count = 0
        des_lst = []
        str = 'HTTP-Method\tURI\tDescription\tAnti-Pattern\tPattern\tComment'
        des_lst.append(str)


        for ur in URI:
            tmp = ur.strip().split(">>")
            #print(tmp)
            line = tmp[1].strip()
            if len(tmp) == 4:
                tmp[3] = ' '.join(tmp[3].split())
                tmp[2] = f"{tmp[2]} {tmp[3]}"


            #print(line)
            #uri_nodes = uri.split("/")
            #print(uri_nodes)
            #nodes = [st.strip().replace("[^a-zA-Z0-9]", "") for st in line.split("/")]
            #print(nodes)
            clean = UriCleaning()
            nodes = clean.get_uri_nodes(line)
            #print(nodes)
            #for new in nodes:
            for i in range(len(nodes)):
                val = clean.set_Acronym(nodes[i])
                if val is not None:
                    for index in range(len(val)):
                        if i + index < len(nodes):
                            nodes[i + index] = val[index]
                        else:
                            nodes.append(val[index])
            #print(nodes)
            #print(splitted_nodes)
            '''splitted_nodes = []
            for node in nodes:
                tmp1 = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', node)
                splitted_nodes.extend(tmp1)
            print(splitted_nodes)'''
        
            pattern = True

            for word in nodes:
                # Perform word lookup operation
                synsets = wn.synsets(word.strip())
                
                if synsets:
                    pattern = pattern | True
                else:
                    pattern = pattern & False

            if not pattern:
                ap_count = ap_count + 1
                non_descriptive_AP.append(f"{line.strip()}\t {AP}")
                str = f"{tmp[0].strip()} \t {tmp[1].strip()} \t {tmp[2].strip()} \t 1 \t 0 \t{AP}"
            elif pattern:
                p_count = p_count + 1
                self_descriptive_P.append(f"{line.strip()}\t {P}")
                str = f"{tmp[0].strip()} \t {tmp[1].strip()} \t {tmp[2].strip()} \t 0 \t 1 \t {P}"
            des_lst.append(str)

        return non_descriptive_AP, self_descriptive_P, p_count, ap_count, des_lst
    

    def detect_contextless(self, URI=None):
        URI = URI if URI else self.URI
        contextless_AP = []
        contextual_P = []
        P = "Contextual Resource Names"
        AP = "Contextless Resource Names"
        p_count = 0
        ap_count = 0
        context_lst = []
        msg = 'HTTP-Method\tURI\tDescription\tAnti-Pattern\tPattern\tComment'
        context_lst.append(msg)


        #print(lines)
        description = []
        nodes = []
        http_method = []
        for ln in URI:
            tmp = ln.split(">>")

            if len(tmp) == 4:
                tmp[3] = ' '.join(tmp[3].split())
                text = f"{tmp[2]} {tmp[3]}"
                description.append(text)
            else:
                description.append(tmp[2])
            nodes.append(tmp[1])
            http_method.append(tmp[0])
        #print(description)
        #print(nodes)


        # Tokenize, remove stopwords, and lemmatize the descriptions
        nlp = spacy.load("en_core_web_lg")
        stop_words = set(stopwords.words('english'))

        '''def preprocess_data(text):
            tokens = word_tokenize(text.lower())
            tokens = [token for token in tokens if token.isalpha() and token not in stop_words]
            doc = nlp(" ".join(tokens))
            lemmatized_tokens = [token.lemma_ for token in doc]
            tokens = [token for token in lemmatized_tokens if len(token) > 1]
            #print(tokens)
            return tokens'''


        def preprocess_word(text):
            doc = nlp(text)
            tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
            return ' '.join(tokens)

        def similarity_calculator(word1, word2):
            word1 = nlp(preprocess_word(word1))
            word2 = nlp(preprocess_word(word2))
            simi = word1.similarity(word2)
            return simi

        '''def simi_average(data):
            if isinstance(data, dict):
                values = list(data.values())  
                average = sum(values) / len(values) if len(values) > 0 else 0  # Calculate average
                return average
            else:
                return data  # Return the input value as it is if not a dictionary'''
        
        clean = UriCleaning()
        #splitted_nodes = clean.get_uri_nodes(line)

        processed_des =[]
        for des in description:
            processed_des.append(clean.preprocess_documentation(des))
        processed_nodes =[]
        for nd in nodes:
            processed_nodes.append(clean.get_uri_nodes(nd))
        
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
        
        for new in processed_des:
            for i in range(len(new)):
                val = clean.set_Acronym(new[i])
                if val is not None:
                    for index in range(len(val)):
                        if i + index < len(new):
                            new[i + index] = val[index]
                        else:
                            new.append(val[index])
        #print(processed_des)

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

        # Display topic words horizontally
        '''table = [["Topic " + str(i+1)] + words for i, words in enumerate(topic_words)]
        print(tabulate(table, headers="firstrow", tablefmt="grid"))'''

        def calculate_similarity(uri_node, topic_words):
            similarity_scores = {}
            for idx, word_list in enumerate(topic_words, start=1):
                word_similarity = {word: similarity_calculator(uri_node, word) for word in word_list}
                similarity_scores[f"Topic {idx}"] = word_similarity
            return similarity_scores

        for method, combined_node, origianl_node, des in zip(http_method, processed_nodes, nodes, description):

            if len(combined_node)<1:
                p_count = p_count + 1
                contextual_P.append(f"-{origianl_node}\t{P}")
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
                p_count = p_count + 1
                contextual_P.append(f"{origianl_node.strip()}\t {P}")
                msg = f"{method.strip()}\t{origianl_node.strip()}\t{des.strip()} \t 0 \t 1 \t {P}"
            else:
                #print("contextless")
                ap_count = ap_count + 1
                contextless_AP.append(f"{origianl_node.strip()}\t {AP}")
                msg = f"{method.strip()}\t{origianl_node.strip()}\t{des.strip()} \t 1 \t 0 \t {AP}"
            context_lst.append(msg)
        return contextless_AP, contextual_P, p_count, ap_count, context_lst
    




    def detect_non_hierarchical_nodes(self, URI=None):
        URI = URI if URI else self.URI
        P = "Hierarchical Nodes"
        AP = "Non-hierarchical Nodes"
        non_hierarchy_result_AP = []
        non_hierarchy_result_P = []
        p_count = 0
        ap_count = 0
        hier_lst = []
        str = 'HTTP-Method\tURI\tDescription\tAnti-Pattern\tPattern\tComment'
        hier_lst.append(str)

        for ur in URI:
            tmp = ur.strip().split(">>")
            #print(tmp)
            uri = tmp[1].strip()

            if len(tmp) == 4:
                tmp[3] = ' '.join(tmp[3].split())
                tmp[2] = f"{tmp[2]} {tmp[3]}"

            #print(uri)
            clean = UriCleaning()
            nodes = clean.get_uri_nodes(uri)

            #for new in nodes:
            for i in range(len(nodes)):
                val = clean.set_Acronym(nodes[i])
                if val is not None:
                    for index in range(len(val)):
                        if i + index < len(nodes):
                            nodes[i + index] = val[index]
                        else:
                            nodes.append(val[index])
            #print(processed_nodes)
                            

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
                non_hierarchy_result_AP.append(f"{uri.strip()}\t{AP}\t{result_information}")
                str = f"{tmp[0].strip()} \t {tmp[1].strip()} \t {tmp[2].strip()} \t 1 \t 0 \t {result_information}"
            else:
                p_count = p_count + 1
                non_hierarchy_result_P.append(f"{uri.strip()}\t{P}\t{result_information}")
                str = f"{tmp[0].strip()} \t {tmp[1].strip()} \t {tmp[2].strip()} \t 0 \t 1 \t {result_information}"
            hier_lst.append(str)
        return non_hierarchy_result_AP, non_hierarchy_result_P, p_count, ap_count, hier_lst
    

    



    def detect_less_cohesive_documentation(self, URI):    
        description = []
        nodes = []
        http_method = []
        for ln in URI:
            tmp = ln.split(">>")
            if len(tmp) == 4:
                tmp[3] = ' '.join(tmp[3].split())
                text = f"{tmp[2]} {tmp[3]}"
                description.append(text)
            else:
                description.append(tmp[2])
            nodes.append(tmp[1])
            http_method.append(tmp[0])
        #print(description)
        #print(nodes)
            
        P="Pertinent Documentation"
        AP="Non-pertinent Documentation"
        less_cohesive_AP = []
        less_cohesive_P = []
        p_count = 0
        ap_count = 0

        cohisive_lst = []
        msg = 'HTTP-Method\tURI\tDescription\tAnti-Pattern\tPattern\tComment'
        cohisive_lst.append(msg)


        # Tokenize, remove stopwords, and lemmatize the descriptions
        nlp = spacy.load("en_core_web_lg")
        stop_words = set(stopwords.words('english'))

        '''def preprocess_data(text):
            tokens = word_tokenize(text)
            tokens = [token for token in tokens if token.isalpha() and token not in stop_words]
            doc = nlp(" ".join(tokens))
            lemmatized_tokens = [token.lemma_ for token in doc]
            tokens = [token for token in lemmatized_tokens if len(token) > 1]
            return tokens'''


        def preprocess_word(text):
            doc = nlp(text)
            tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
            return ' '.join(tokens)

        def similarity_calculator(word1, word2):
            word1 = nlp(preprocess_word(word1))
            word2 = nlp(preprocess_word(word2))
            simi = word1.similarity(word2)
            return simi

        '''def simi_average(data):
            if isinstance(data, dict):
                values = list(data.values())  
                average = sum(values) / len(values) if len(values) > 0 else 0  # Calculate average
                return average
            else:
                return data  # Return the input value as it is if not a dictionary'''
        
        clean = UriCleaning()
        #splitted_nodes = clean.get_uri_nodes(line)
        
        processed_des =[]
        for des in description:
            processed_des.append(clean.preprocess_documentation(des))
            #print(f"{des}--------{p_des}")
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
        
        for new in processed_des:
            for i in range(len(new)):
                val = clean.set_Acronym(new[i])
                if val is not None:
                    for index in range(len(val)):
                        if i + index < len(new):
                            new[i + index] = val[index]
                        else:
                            new.append(val[index])
        #print(processed_des)
        
        def calculate_similarity(uri_node, topic_words):
            similarity_scores = {}
            for idx, word_list in enumerate(topic_words, start=1):
                word_similarity = {word: similarity_calculator(uri_node, word) for word in word_list}
                similarity_scores[f"Topic {idx}"] = word_similarity
            return similarity_scores

        for method, combined_node, documentation, node_uri, des in zip(http_method, processed_nodes,processed_des, nodes, description):
            # Calculate similarity for each individual node
            topics = len(combined_node)
            #print(topics)
            print(combined_node)
            
            print(documentation)
            if len(documentation)<1 or len(combined_node) < 1 :
                p_count = p_count + 1
                less_cohesive_P.append(f"-{node_uri.strip()}\t{P}\t{des}")
                msg = f"{method.strip()}\t{node_uri.strip()}\t{des.strip()} \t 0 \t 1 \t {P}"
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
                print(f"  {topic_name}:")
                tmp = 0
                for node, word_scores in node_word_similarity.items():
                    score = word_scores.get(topic_name, {})
                    print(f"    {node}: {score}")  # Print scores for each node under the topic
                    #tmp1 = simi_average(score)
                    #print(tmp1)
                    max_value_key = max(score, key=score.get)
                    max_value = score[max_value_key]
                    #print(max_value)
                    tmp += max_value
                avg_tmp = tmp / len(node_word_similarity)
                topic_avg.append(avg_tmp)
                print(f"  Average Similarity for {topic_name}: {avg_tmp}\n")
            
            print(f"Total Average for All Topics: {topic_avg}\n")
            #for avg in topic_avg:
            print(max(topic_avg))
            if round(max(topic_avg), 1) >= 0.5:
                #print("cohisive")
                p_count = p_count + 1
                less_cohesive_P.append(f"-{node_uri.strip()}\t{P}\t{des.strip()}")
                msg = f"{method.strip()}\t{node_uri.strip()}\t{des.strip()} \t 0 \t 1 \t {P}"
            else:
                #print("less_cohisive")
                ap_count = ap_count + 1
                less_cohesive_AP.append(f"-{node_uri.strip()}\t{AP}\t{des.strip()}")
                msg = f"{method.strip()}\t{node_uri.strip()}\t{des.strip()} \t 1 \t 0 \t {AP}"
            cohisive_lst.append(msg)
            
        return less_cohesive_AP, less_cohesive_P, p_count, ap_count, cohisive_lst
    


    def detect_inconsistent_documentations(self, URI=None):
        URI = URI if URI else self.URI

        post = ["return", "returns", "delete", "deletes", "update", "modify", "query", "list", "lists", "check", "checks", "verify", "get", "gets"]
        delete = ["get", "gets", "find", "finds", "search", "check", "list", "verify", "get", "gets"]
        put = ["delete", "deletes", "creates", "finds", "create", "find", "search", "checks", "lists", "check", "list"]
        get = ["delete", "deletes", "updates", "update", "creates", "create"]
        
        description = []
        nodes = []
        http_method = []
        incos_lst = []
        msg = 'HTTP-Method\tURI\tDescription\tAnti-Pattern\tPattern\tComment'
        incos_lst.append(msg)

        for ln in URI:
            tmp = ln.split(">>")
            if len(tmp) == 4:
                tmp[3] = ' '.join(tmp[3].split())
                text = f"{tmp[2]} {tmp[3]}"
                description.append(text)
            else:
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
            lemmatized_tokens = [f'{token}' for token in doc]
            return lemmatized_tokens

        P = "Consistent Documentation"
        AP = "Inconsistent Documentation"

        inconsistent_documentation_AP = []
        inconsistent_documentation_P = []
        p_count = 0
        ap_count = 0
        
        clean = UriCleaning()

        for h_method, uri, documentation in zip(http_method, nodes, description):
            #documentation = documentation.strip()
            method = h_method.lower().strip()
            #print(method)
            words = preprocess_data(documentation)
            #print(words)
            #uri = clean.get_uri_nodes(node)
            #print(words)
            #print(uri)
            #print("\n\n")
            
            if method == "get":
                #if any(item in get for item in words):
                if any(item in get for item in words):
                    msg = f"{h_method.strip()}\t{uri.strip()}\t{documentation.strip()} \t 1 \t 0 \t {AP}"
                    inconsistent_documentation_AP.append(f"{h_method.strip()}\t{uri.strip()}\t{AP}\t{documentation.strip()}")
                    ap_count += 1
                else:
                    msg = f"{h_method.strip()}\t{uri.strip()}\t{documentation.strip()} \t 0 \t 1 \t {P}"
                    inconsistent_documentation_P.append(f"{h_method.strip()}\t{uri}\t{P.strip()}\t{documentation.strip()}")
                    p_count += 1
            elif method == "delete":
                if any(item in delete for item in words):
                    msg = f"{h_method.strip()}\t{uri.strip()}\t{documentation.strip()} \t 1 \t 0 \t {AP}"
                    inconsistent_documentation_AP.append(f"{h_method.strip()}\t{uri.strip()}\t{AP}\t{documentation.strip()}")
                    ap_count += 1
                else:
                    msg = f"{h_method.strip()}\t{uri.strip()}\t{documentation.strip()} \t 0 \t 1 \t {P}"
                    inconsistent_documentation_P.append(f"{h_method.strip()}\t{uri.strip()}\t{P}\t{documentation.strip()}")
                    p_count += 1
            elif method == "put":
                if any(item in put for item in words):
                    msg = f"{h_method.strip()}\t{uri.strip()}\t{documentation.strip()} \t 1 \t 0 \t {AP}"
                    inconsistent_documentation_AP.append(f"{h_method.strip()}\t{uri}\t{AP}\t{documentation.strip()}")
                    ap_count += 1
                else:
                    msg = f"{h_method.strip()}\t{uri.strip()}\t{documentation.strip()} \t 0 \t 1 \t {P}"
                    inconsistent_documentation_P.append(f"{h_method.strip()}\t{uri}\t{P}\t{documentation.strip()}")
                    p_count += 1
            elif method == "post":
                if any(item in post for item in words):
                    msg = f"{h_method.strip()}\t{uri.strip()}\t{documentation.strip()} \t 1 \t 0 \t {AP}"
                    inconsistent_documentation_AP.append(f"{h_method.strip()}\t{uri}\t{AP}\t{documentation.strip()}")
                    ap_count += 1
                else:
                    msg = f"{h_method.strip()}\t{uri.strip()}\t{documentation.strip()} \t 0 \t 1 \t {P}"
                    inconsistent_documentation_P.append(f"{h_method.strip()}\t{uri}\t{P}\t{documentation.strip()}")
                    p_count += 1
            else:
                msg = f"{h_method.strip()}\t{uri.strip()}\t{documentation.strip()} \t 0 \t 1 \t {P}"
                inconsistent_documentation_P.append(f"{h_method.strip()}\t{uri.strip()}\t{P}\t{documentation.strip()}")
                p_count += 1
            incos_lst.append(msg)

        return inconsistent_documentation_AP, inconsistent_documentation_P, p_count, ap_count, incos_lst



    

