from myapp.search.search_algorithms.tf_idf import rank_documents
from myapp.search.search_algorithms.utils import preprocess

def our_rank_documents_retweets(terms, docs, index, idf, tf, tweets):
    """
    Perform the ranking of the results of a search based on the tf-idf weights and number of retweets

    Argument:
    terms -- list of query terms
    docs -- list of documents, to rank, matching the query
    index -- inverted index data structure
    idf -- inverted document frequencies
    tf -- term frequencies

    Returns:
    doc_scores -- list of scores
    """
    pre_scores = rank_documents(terms, docs, index, idf, tf)
    new_scores = []
    new_scores = [[tweets[id].retweets * score, id] if id in tweets else [0, id]  for score, id in pre_scores]

    new_scores.sort(reverse=True)
    return new_scores


def search_tf_idf_rt(query, index, tf, idf, tweets):
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
    doc_scores = our_rank_documents_retweets(query, docs, index, idf, tf, tweets)
    return doc_scores
