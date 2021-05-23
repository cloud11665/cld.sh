from functools import lru_cache, wraps
import datetime
import psutil

def timed_lru_cache(seconds:int=60, maxsize=None):
	def wrapper_cache(func):
		func = lru_cache(maxsize=maxsize)(func)
		func.lifetime = datetime.timedelta(seconds=seconds)
		func.expiration = datetime.datetime.utcnow() + func.lifetime

		@wraps(func)
		def wrapped_func(*args, **kwargs):
			if datetime.datetime.utcnow() >= func.expiration:
				func.cache_clear()
				func.expiration = datetime.datetime.utcnow() + func.lifetime

			return func(*args, **kwargs)

		return wrapped_func

	return wrapper_cache

def gh_parse_event(event):
	if event["type"] == "CommitCommentEvent":
		return None

	if event["type"] == "CreateEvent":
		return f'Created a repository <a class="ghlink" href="{event["repo"]["url"]}">{event["repo"]["name"]}</a>'

	if event["type"] == "DeleteEvent":
		return None

	if event["type"] == "ForkEvent":
		return f'Forked <a class="ghlink" href="{event["payload"]["forkee"]["html_url"]}">{event["payload"]["forkee"]["full_name"]}</a> from <a class="ghlink" href="{event["repo"]["url"]}">{event["repo"]["name"]}</a>'

	if event["type"] == "GollumEvent":
		return None

	if event["type"] == "IssueCommentEvent":
		return None

	if event["type"] == "IssuesEvent":
		action = event["payload"]["action"]
		if action == "opened":
			return f'Opened an <a class="ghlink" href="{event["payload"]["issue"]["html_url"]}">issue</a> in <a class="ghlink" href="{event["repo"]["url"]}">{event["repo"]["name"]}</a> that recived {event["payload"]["issue"]["comments"]} {["comment","comments"][event["payload"]["issue"]["comments"]>1]}'
		elif action == "closed":
			return f'Closed an <a class="ghlink" href="{event["payload"]["issue"]["html_url"]}">issue</a> in <a class="ghlink" href="{event["repo"]["url"]}">{event["repo"]["name"]}</a>'
		elif action == "reopened":
			return f'Reopened an <a class="ghlink" href="{event["payload"]["issue"]["html_url"]}">issue</a> in <a class="ghlink" href="{event["repo"]["url"]}">{event["repo"]["name"]}</a>'
		elif action == "assigned":
			return None
		elif action == "unassigned":
			return None
		elif action == "labeled":
			return None
		elif action == "unlabeled":
			return None
		else:
			return None

	if event["type"] == "MemberEvent":
		return None

	if event["type"] == "PublicEvent":
		return f'Made <a class="ghlink" href="{event["repo"]["url"]}">{event["repo"]["name"]}</a> public'

	if event["type"] == "PullRequestEvent":
		action = event["payload"]["action"]
		if action == "opened":
			return f'Opened a <a class="ghlink" href="{event["payload"]["pull_request"]["_links"]["html"]["href"]}">pull request</a> in <a class="ghlink" href="{event["repo"]["url"]}">{event["repo"]["name"]}</a>'
		elif action == "closed":
			return f'Closed a <a class="ghlink" href="{event["payload"]["pull_request"]["_links"]["html"]["href"]}">pull request</a> in <a class="ghlink" href="{event["repo"]["url"]}">{event["repo"]["name"]}</a>'
		elif action == "reopened":
			return f'Reopened a <a class="ghlink" href="{event["payload"]["pull_request"]["_links"]["html"]["href"]}">pull request</a> in <a class="ghlink" href="{event["repo"]["url"]}">{event["repo"]["name"]}</a>'
		elif action == "assigned":
			return None
		elif action == "unassigned":
			return None
		elif action == "review_requested":
			return None
		elif action == "review_request_removed":
			return None
		elif action == "labeled":
			return None
		elif action == "unlabeled":
			return None
		elif action == "synchronize":
			return None
		else:
			return None

	if event["type"] == "PullRequestReviewEvent":
		return None

	if event["type"] == "PullRequestReviewCommentEvent":
		return None

	if event["type"] == "PushEvent":
		commits = event["payload"]["commits"]
		if len(commits) == 1:
			return f'Pushed {len(commits)} commit to <a class="ghlink" href="{event["repo"]["url"]}">{event["repo"]["name"]}</a>'
		else:
			return f'Pushed {len(commits)} commits to <a class="ghlink" href="{event["repo"]["url"]}">{event["repo"]["name"]}</a>'

	if event["type"] == "ReleaseEvent":
		return f'Released <a class="ghlink" href="{event["payload"]["release"]["html_url"]}">{event["payload"]["release"]["tag_name"]}</a> of <a class="ghlink" href="{event["repo"]["url"]}">{event["repo"]["name"]}</a>'

	if event["type"] == "SponsorshipEvent":
		return None
	if event["type"] == "WatchEvent":
		return None #(f'Starred', event['repo']['name'])


@timed_lru_cache(15)
def cpu_usage():
	return psutil.cpu_percent(0.05)
