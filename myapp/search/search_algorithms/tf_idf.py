from collections import defaultdict
import numpy as np
import collections
from numpy import linalg as la
from myapp.search.search_algorithms.utils import preprocess

def rank_documents(terms, docs, index, idf, tf):
    """
    Perform the ranking of the results of a search based on the tf-idf weights

    Argument:
    terms -- list of query terms
    docs -- list of documents, to rank, matching the query
    index -- inverted index data structure
    idf -- inverted document frequencies
    tf -- term frequencies

    Returns:
    doc_scores -- list of scores
    """

    doc_vectors = defaultdict(lambda: [0] * len(terms)) # Call doc_vectors[k] for a nonexistent key k, the key-value pair (k,[0]*len(terms)) will be automatically added to the dictionary
    query_vector = [0] * len(terms)

    # compute the norm for the query tf
    query_terms_count = collections.Counter(terms)  # get the frequency of each term in the query.

    query_norm = la.norm(list(query_terms_count.values()))

    for termIndex, term in enumerate(terms):  #termIndex is the index of the term in the query
        if term not in index:
            continue

        ## Compute tf*idf(normalize TF as done with documents)
        query_vector[termIndex]=query_terms_count[term]/idf[term] * query_norm

        # Generate doc_vectors for matching docs
        for doc_index, (doc, postings) in enumerate(index[term]):

            #tf[term][0] will contain the tf of the term "term" in the doc 26
            if doc in docs:
                doc_vectors[doc][termIndex] = tf[term][doc_index] * idf[term]
    # Calculate the score of each doc
    # compute the cosine similarity between queryVector and each docVector:

    doc_scores = [[np.dot(curDocVec, query_vector), doc] for doc, curDocVec in doc_vectors.items() ]
    doc_scores.sort(reverse=True)

    return doc_scores

def search_tf_idf(query, index, tf, idf):
    """
    output is the list of documents that contain all of the query terms.
    So, we will get the list of documents for each query term, and take the intersection of them.

    Argument:
    query -- name of the query
    index -- created index

    Returns:
    doc_scores -- list of scores
    """
    query = preprocess(query)
    docs = set()

    # Initialize docs with the document IDs containing the first term
    first_term = query[0]
    try:
        # store in term_docs the ids of the docs that contain "term"
        docs = set(posting[0] for posting in index[first_term])
    except:

        return []

    # Iterate through the second term of the query
    for term in query[1:]:
        try:
            term_docs = set(posting[0] for posting in index[term])
            # Take the intersection of docs and term_docs
            docs = docs.intersection(term_docs)
        except:

            return []

    docs = list(docs)
    doc_scores = rank_documents(query, docs, index, idf, tf)
    return doc_scores

