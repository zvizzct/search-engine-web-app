import random

from myapp.search.algorithms import search_in_corpus
from myapp.search.objects import ResultItem, Document



def build_demo_results(corpus: dict, search_id):
    """
    Helper method, just to demo the app
    :return: a list of demo docs sorted by ranking
    """
    res = []
    size = len(corpus)
    ll = list(corpus.values())
    for index in range(random.randint(0, 40)):
        item: Document = ll[random.randint(0, size)]
        res.append(ResultItem(item.id, item.title, item.description, item.doc_date,
                              "doc_details?id={}&search_id={}&param2=2".format(item.id, search_id), random.random()))

    # for index, item in enumerate(corpus['Id']):
    #     # DF columns: 'Id' 'Tweet' 'Username' 'Date' 'Hashtags' 'Likes' 'Retweets' 'Url' 'Language'
    #     res.append(DocumentInfo(item.Id, item.Tweet, item.Tweet, item.Date,
    #                             "doc_details?id={}&search_id={}&param2=2".format(item.Id, search_id), random.random()))

    # simulate sort by ranking
    res.sort(key=lambda doc: doc.ranking, reverse=True)
    return res


class SearchEngine:
    """educational search engine"""

    def search(self, search_query, search_id, corpus, algorithm, page=1, limit=10):
        print("Search query:", search_query)

        if(not search_query): return [], 0, 1
        all_results = search_in_corpus(search_query, search_id, corpus, algorithm)
        total_pages = -(-len(all_results) // limit)

        start = (page - 1) * limit
        end = start + limit
        print(start,end)

        paginated_results = all_results[start:end]


        return paginated_results, len(all_results), total_pages
