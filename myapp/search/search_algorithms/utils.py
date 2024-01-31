from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import re
import json

def remove_emojis(text):
    """
    Remove all emojis from the given text

    Argument:
    text -- the text to clean

    Returns:
    text - the same text without emojis
    """

    #All emojis are represented in Unicode, so we can remove them by using RE
    #Regular expression found at https://gist.github.com/slowkow/7a7f61f495e3dbb7e3d767f97bd7304b
    emojis_expression = re.compile("["
                            u"\U0001F600-\U0001F64F"  # emoticons
                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            u"\U00002500-\U00002BEF"  # chinese char
                            u"\U00002702-\U000027B0"
                            u"\U00002702-\U000027B0"
                            u"\U000024C2-\U0001F251"
                            u"\U0001f926-\U0001f937"
                            u"\U00010000-\U0010ffff"
                            u"\u2640-\u2642"
                            u"\u2600-\u2B55"
                            u"\u200d"
                            u"\u23cf"
                            u"\u23e9"
                            u"\u231a"
                            u"\ufe0f"  # dingbats
                            u"\u3030"
                            "]+", flags=re.UNICODE)

    return re.sub(emojis_expression, "", text)

def preprocess(text):
    """
    Clean and tokenize the text

    Argument:
    text -- the text to clean

    Returns:
    text - the list of tokens obtained from the input text.
    """
    stemmer = PorterStemmer()
    stop_words = stopwords.words("english")
    punctuation = r"[!¡?¿.:,;()\[\]{}\-\'\"]"

    text = remove_emojis(text) #Remove emojis
    text = text.strip() #Remove whitespaces at the beginning and at the end
    text = text.lower() ## Transform in lowercase
    text = re.sub(punctuation, "", text) ## Eliminate puntuation marks
    text = text.split() ## Tokenize the text to get a list of terms
    text = [token for token in text if token not in stop_words] ## Eliminate the stopwords
    text = [stemmer.stem(token) for token in text] ## Perform stemming

    return text


def create_tf_idf_index(index_path):
    with open(index_path) as fp:
        tf_idf_index = json.load(fp)

    tf = tf_idf_index["tf"]
    idf = tf_idf_index["idf"]
    index = tf_idf_index["index"]

    return tf, idf, index