import flask
import time
import requests

from utils import *

app = flask.Flask(__name__)

@app.before_request
def before_request():
	flask.g.request_start_time = time.time()
	flask.g.request_time = lambda: f"{1000*(time.time() - flask.g.request_start_time):.2f}ms"

@timed_lru_cache(15*60)
def api_status():
	return requests.get("https://sabat.dev", auth=("Cloud11665","")).ok

@timed_lru_cache(5*60)
def gh_activity():
	resp = requests.get((
		"https://api.github.com/users/Cloud11665/events/public"
		"?per_page=64"
		"&page=0"
	))
	resp = resp.json()
	events = [gh_parse_event(x) for x in resp]
	events = [*filter(bool, events)]

	return events

def template_data():
	ts = 0x12BFFA0CDB0 * 1e-3
	utc_off = datetime.datetime.fromtimestamp(ts) - datetime.datetime.utcfromtimestamp(ts)
	mins = utc_off // datetime.timedelta(minutes=1)

	return {
		"offset": mins,
		"api_status": api_status(),
		"cpu_usage": cpu_usage(),
		"urls":["/","/blog", "/about", "/projects"]
		}

@app.route("/")
def index():
	return flask.render_template("./index.html"
		,**template_data()
		,selected="/"
		,activities=gh_activity()
	)

@app.route("/blog")
def blog():
	return flask.render_template("./blog.html"
		,**template_data()
		,selected="/blog"
	)

@app.route("/about")
def about():
	return flask.render_template("./about.html"
		,**template_data()
		,selected="/about"
	)

@app.route("/projects")
def projects():
	return flask.render_template("./projects.html"
		,**template_data()
		,selected="/projects"
	)

app.run(debug=True)