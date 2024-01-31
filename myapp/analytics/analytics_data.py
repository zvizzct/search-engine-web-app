import json
import random
from datetime import datetime
import uuid

class AnalyticsData:
    """
    An in memory persistence object.
    Declare more variables to hold analytics tables.
    """
    # statistics table 1
    # fact_clicks is a dictionary with the click counters: key = doc id | value = click counter
    fact_clicks = dict([])

    # statistics table 2
    fact_queries = []

    # statistics table 3
    fact_three = dict([])

    http_requests=[] 
    http_sessions={}
    query_terms={}   
    doc_clicks={} 
    user_context={} 
    session_queries={}


    def save_query_terms(self, terms: str):
        split_terms = terms.split()
        for term in split_terms:
            if(term in self.query_terms):
                current_term:QueryTerm = self.query_terms[term]
                current_term.count += 1
                current_term.used_with.union([t for t in split_terms if term != t])
            else:
                self.query_terms[term] = QueryTerm(term, 1, set([t for t in split_terms if term != t]), datetime.now())

        return uuid.uuid4()

    def register_http_request(self, request_data):
        self.http_requests.append(request_data)

    def start_session(self, session_id, user_data):
        self.http_sessions[session_id] = {
            "start_time": datetime.now(),
            "user_data": user_data,
            "queries": []
        }

    def end_session(self, session_id):
        if session_id in self.http_sessions:
            self.http_sessions[session_id]["end_time"] = datetime.now()
    
    def save_current_user(self, session_id, user_data):
        self.user_context[session_id] = user_data

    def save_session_queries(self, session_id, query):
        if session_id in self.session_queries:
            self.session_queries[session_id].append(query)
        else:
            self.session_queries[session_id] = [query]
        
class ClickedDoc:
    def __init__(self, doc_id, description, counter):
        self.doc_id = doc_id
        self.description = description
        self.counter = counter

    def to_json(self):
        return self.__dict__

    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)

class QueryTerm:
    def __init__(self, term, count, used_with, date):
        self.term = term
        self.count = count
        self.used_with:set = used_with
        self.date = date

    def to_json(self):
        return {
            "term": self.term,
            "count": self.count,
            "used_with": list(self.used_with),
            "date": str(self.date)
        }

    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)