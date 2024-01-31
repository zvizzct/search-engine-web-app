from numpy import dot
import numpy.linalg as la
from numpy.linalg import norm
import numpy as np
from myapp.search.search_algorithms.utils import preprocess
from gensim.models import Word2Vec


def create_word2vec(tweets):
    #Create Word2Vec model
    model = Word2Vec(sentences=[preprocess(tweet.description) for tweet in tweets.values()], vector_size=100, window=5, min_count=1, workers=4)
    return model

def vectorize_tweets(model, tweets):
    tweet_vectors = []
    filtered_tweets = []

    #Iterate through each tweet
    for tweet in tweets.values():
        words = [word for word in preprocess(tweet.description) if word in model.wv.key_to_index]
        #Check if the word exits in the model created
        if words:
            tweet_vector = np.mean([model.wv[word] for word in words], axis=0)
            tweet_vector /= la.norm(tweet_vector)
            tweet_vectors.append(tweet_vector)
            filtered_tweets.append(tweet)

    #Transform into an array
    tweet_vectors_np = np.array(tweet_vectors)

    return tweet_vectors_np


def rank_documents_word2vec(query_vector, tweet_vectors):
    """
    Rank documents based on cosine similarity with the query vector.

    Arguments:
    query_vector -- vector representation of the query
    tweet_vectors -- list of tweet vectors

    Returns:
    ranked_indices -- list of tuples containing score and index of ranked tweets
    """
    #Calculate the cosine similarity of each tweet
    cos_similarities = [(dot(query_vector, tweet_vec) / (norm(query_vector) * norm(tweet_vec)), i)
                        for i, tweet_vec in enumerate(tweet_vectors)]
    #Sort them in descending order
    ranked_indices = sorted(cos_similarities, key=lambda x: x[0], reverse=True)
    return ranked_indices

def search_word2vec(query, model, tweet_vectors, tweets):
    """
    Search for documents that contain the query terms using Word2Vec representations.

    Arguments:
    query -- the search query
    model -- Word2Vec model
    tweet_vectors -- list of tweet vectors
    tweets -- list of original tweets

    Returns:
    filtered_ranked_tweet_indices -- list of indices of ranked tweets based on the query
    """
    docid_vectorid = {tweet.id: i for i, tweet in enumerate(tweets.values())}

    query_preprocessed = preprocess(query)
    
    query_words = set(word for word in query_preprocessed if word in model.wv.key_to_index)

    preprocessed_tweets = [[preprocess(tweet.description), tweet.id] for tweet in tweets.values()]

    relevant_tweet_indices = set()

    for word in query_words:
        relevant_tweet_indices.update([i for tweet, i in preprocessed_tweets if word in tweet])
    if not relevant_tweet_indices:
        return []
    
    query_vector = np.mean([model.wv[word] for word in query_words], axis=0)
    query_vector /= norm(query_vector)
    relevant_tweet_vectors = [tweet_vectors[docid_vectorid[i]] for i in relevant_tweet_indices]

    ranked_tweet_indices = rank_documents_word2vec(query_vector, relevant_tweet_vectors)

    filtered_ranked_tweet_indices = [(score, list(relevant_tweet_indices)[index]) for score, index in ranked_tweet_indices]
    return filtered_ranked_tweet_indices
