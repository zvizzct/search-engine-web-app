import os
import datetime
import uuid
import nltk
from json import JSONEncoder

import httpagentparser 
from flask import Flask, redirect, render_template, session, request, url_for

from myapp.analytics.analytics_data import AnalyticsData, ClickedDoc
from myapp.search.load_corpus import load_corpus
from myapp.search.objects import Document, StatsDocument
from myapp.search.search_engine import SearchEngine

def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)

_default.default = JSONEncoder().default  
JSONEncoder.default = _default  

app = Flask(__name__)
app.secret_key = 'afgsreg86sr897b6st8b76va8er76fcs6g8d7'  
app.session_cookie_name = 'IRWA_SEARCH_ENGINE'  

search_engine = SearchEngine()
analytics_data = AnalyticsData()

full_path = os.path.realpath(__file__)
path, filename = os.path.split(full_path)
file_path = os.path.join(path, "Rus_Ukr_war_data.json")
corpus = load_corpus(file_path)
print("Loaded corpus. First element:", list(corpus.values())[0])

@app.before_request
def before_request_func():
    session_id = session.get('session_id')

    if session_id is None or (session_id in analytics_data.http_sessions and 'end_time' in analytics_data.http_sessions[session_id]):
        session['session_id'] = str(uuid.uuid4())
        session_id = session['session_id']

    request_data = {
        "path": request.path,
        "method": request.method,
        "session_id": session_id,
        "timestamp": datetime.datetime.now(),
    }
    analytics_data.register_http_request(request_data)

@app.route('/')
def index():
    print("Starting home URL /...")

    user_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    agent = httpagentparser.detect(user_agent)

    session_id = session.get('session_id')

    session_data = {"session_agent": agent, "session_ip": user_ip}
    analytics_data.start_session(session_id, session_data)

    user_data = {"session_id": session_id, "agent": agent, "user_ip": user_ip}
    analytics_data.save_current_user(session_id, user_data)

    print(user_data)

    return render_template('index.html', page_title="Welcome", session_id=session_id)



@app.route('/search', methods=['GET', 'POST'])
def search_form_post():
    if request.method == 'POST':
        search_query = request.form['search-query']
        algorithm = request.form["algorithm"]
        # Guarda la consulta de búsqueda y el algoritmo en la sesión
        session['search_query'] = search_query
        session['algorithm'] = algorithm
        # Redirige a la ruta de búsqueda con los parámetros adecuados
        return redirect(url_for('search_results', search_query=search_query, algorithm=algorithm))
    
    # El resto del código permanece igual

@app.route('/search_results')
def search_results():
    search_query = request.args.get('search_query', session.get('search_query', ''))
    algorithm = request.args.get('algorithm', session.get('algorithm', 'default_algorithm'))
    page = int(request.args.get('page', 1))
    limit = 10
    search_id = analytics_data.save_query_terms(search_query)
    session_id = session.get('session_id')

    # Asumiendo que tienes una función que realiza la búsqueda...
    results, total_results, total_pages = search_engine.search(search_query, search_id, corpus, algorithm, page, limit)

    return render_template('results.html', results_list=results, page_title="Results",
                           found_counter=total_results,
                           current_page=page, total_pages=total_pages,
                           search_query=search_query, algorithm=algorithm,session_id=session_id)

@app.route('/doc_details', methods=['GET'])
def doc_details():
    # getting request parameters:
    # user = request.args.get('user')

    print("doc details session: ")
    print(session)



    # get the query string parameters from request
    clicked_doc_id = int(request.args["id"])
    #p1 = int(request.args["search_id"])  # transform to Integer
    #p2 = int(request.args["param2"])  # transform to Integer
    print("click in id={}".format(clicked_doc_id))

    # store data in statistics table 1
    if clicked_doc_id in analytics_data.fact_clicks.keys():
        analytics_data.fact_clicks[clicked_doc_id] += 1
    else:
        analytics_data.fact_clicks[clicked_doc_id] = 1

    print("fact_clicks count for id={} is {}".format(clicked_doc_id, analytics_data.fact_clicks[clicked_doc_id]))
    session_id = session.get('session_id')

    doc = corpus[clicked_doc_id]
    return render_template('doc_details.html', document=doc,session_id=session_id)


@app.route('/stats', methods=['GET'])
def stats():
    """
    Show statistics including HTTP requests, sessions, and user context.
    """
    # Extract data from analytics_data object
    http_requests = analytics_data.http_requests
    http_sessions = analytics_data.http_sessions
    user_context = analytics_data.user_context
    session_id = session.get('session_id')

    # Return the template with the extracted data
    return render_template('stats.html', 
                           http_requests=http_requests, 
                           http_sessions=http_sessions, 
                           user_context=user_context,session_id=session_id)

    # ### End replace with your code ###


@app.route('/dashboard', methods=['GET'])
def dashboard():
    visited_docs = []
    print(analytics_data.fact_clicks.keys())
    for doc_id in analytics_data.fact_clicks.keys():
        d: Document = corpus[int(doc_id)]
        doc = ClickedDoc(doc_id, d.description, analytics_data.fact_clicks[doc_id])
        visited_docs.append(doc)

    # simulate sort by ranking
    visited_docs.sort(key=lambda doc: doc.counter, reverse=True)

    visited_docs = [doc.to_json() for doc in visited_docs]

    query_terms = [term.to_json() for term in analytics_data.query_terms.values()]
    session_id = session.get('session_id')

    return render_template('dashboard.html', visited_docs=visited_docs, query_terms=query_terms,session_id=session_id)


@app.route('/sentiment')
def sentiment_form():
    session_id = session.get('session_id')
    return render_template('sentiment.html', session_id=session_id)


@app.route('/sentiment', methods=['POST'])
def sentiment_form_post():
    session_id = session.get('session_id')
    text = request.form['text']
    nltk.download('vader_lexicon')
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()
    score = ((sid.polarity_scores(str(text)))['compound'])
    return render_template('sentiment.html', score=score, session_id=session_id)

@app.route('/end_session', methods=['POST'])
def end_session_route():
    session_id = session.get('session_id')
    if session_id:
        analytics_data.end_session(session_id)
        session.pop('session_id', None)

    return redirect(url_for('index'))

# if __name__ == "__main__":
#     app.run(port=8088, host="0.0.0.0", threaded=False, debug=True)
