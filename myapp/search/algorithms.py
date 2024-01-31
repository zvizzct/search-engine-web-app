#Imports
import nltk
from myapp.search.load_corpus import load_corpus
from myapp.search.objects import ResultItem, Document
from myapp.search.search_algorithms.tf_idf import search_tf_idf
from myapp.search.search_algorithms.like_tf_idf import search_tf_idf_likes
from myapp.search.search_algorithms.retweets_tf_idf import search_tf_idf_rt
from myapp.search.search_algorithms.utils import create_tf_idf_index
from myapp.search.search_algorithms.word2vec import create_word2vec
from myapp.search.search_algorithms.word2vec import vectorize_tweets
from myapp.search.search_algorithms.word2vec import search_word2vec

nltk.download("stopwords")

index_path = "tf-idf_idx.json"
file_path = "Rus_Ukr_war_data.json"

#Create tf-idf index and Word2vec model
tf, idf, index = create_tf_idf_index(index_path)

tweets = load_corpus(file_path)

#Create the Word2Vec model
model = create_word2vec(tweets)

# 2. Vectorize all the tweets
tweet_vectors_np = vectorize_tweets(model, tweets)


def search_in_corpus(query, search_id, corpus: [Document], algorithm):

    if(algorithm == "Normal_tf-idf"):
        # 2. Apply normal tf-idf ranking
        results = [ResultItem(tweet_id,
                              corpus[tweet_id].title,
                              corpus[tweet_id].username,
                              corpus[tweet_id].description,
                              corpus[tweet_id].doc_date,
                              corpus[tweet_id].url,
                              score) for score, tweet_id in search_tf_idf(query, index, tf, idf)]

    elif(algorithm == "Word2Vec"):
        # 2. Apply Word2Vec ranking
        results=[ResultItem(tweet_id,
                              corpus[tweet_id].title,
                              corpus[tweet_id].username,
                              corpus[tweet_id].description,
                              corpus[tweet_id].doc_date,
                              corpus[tweet_id].url,
                              score) for score, tweet_id in search_word2vec(query, model, tweet_vectors_np, corpus)]

    elif(algorithm == "Like_tf-idf"):
        #2. Apply likes ranking
        results=[ResultItem(tweet_id,
                              corpus[tweet_id].title,
                              corpus[tweet_id].username,
                              corpus[tweet_id].description,
                              corpus[tweet_id].doc_date,
                              corpus[tweet_id].url,
                              score) for score, tweet_id in search_tf_idf_likes(query, index, tf, idf, corpus)]

    elif(algorithm == "Retweet_tf-idf"):
        #2. Apply retweet ranking
        results=[ResultItem(tweet_id,
                              corpus[tweet_id].title,
                              corpus[tweet_id].username,
                              corpus[tweet_id].description,
                              corpus[tweet_id].doc_date,
                              corpus[tweet_id].url,
                              score) for score, tweet_id in search_tf_idf_rt(query, index, tf, idf, corpus)]


    return results 