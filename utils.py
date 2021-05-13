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
		return (f"Created", event['repo']['name'])
	if event["type"] == "DeleteEvent":
		return None

	if event["type"] == "ForkEvent":
		return (f"Forked", event['repo']['name'])

	if event["type"] == "GollumEvent":
		return None
	if event["type"] == "IssueCommentEvent":
		return None

	if event["type"] == "IssuesEvent":
		action = event["payload"]["action"]

		if action == "opened":
			text = f"Opened an issue in"
		elif action == "closed":
			text = f"Closed an issue in"
		elif action == "reopened":
			text = f"Reopened an issue in"
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
		return (text, event['repo']['name'])

	if event["type"] == "MemberEvent":
		return None

	if event["type"] == "PublicEvent":
		return (f"Made {event['repo']['name']} public", event['repo']['name'])

	if event["type"] == "PullRequestEvent":
		action = event["payload"]["action"]

		if action == "opened":
			text = f"Opened a pull request in"
		elif action == "closed":
			text = f"Closed a pull request in"
		elif action == "reopened":
			text = f"Reopened a pull request in"
		elif action == "assigned":
			return None
		elif action == "unassigned":
			return None
		elif action == "review_requested":
			text = f"Requested review in"
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
		return (text, event['repo']['name'])

	if event["type"] == "PullRequestReviewEvent":
		return None
	if event["type"] == "PullRequestReviewCommentEvent":
		return None
	if event["type"] == "PushEvent":
		commits = event["payload"]["commits"]
		if len(commits) == 1:
			return (f"Created 1 commit in", event['repo']['name'])
		else:
			return (f"Created {len(commits)} commits in", event['repo']['name'])
	if event["type"] == "ReleaseEvent":
		return (F"Published a new release in", event['repo']['name'])
	if event["type"] == "SponsorshipEvent":
		return None
	if event["type"] == "WatchEvent":
		return None
		return (f"Starred", event['repo']['name'])


@timed_lru_cache(15)
def cpu_usage():
	return psutil.cpu_percent(0.05)
