import os
import unittest
import sys
import requests
from pathlib import Path
import threading
import time
import io
import contextlib
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

import jinja2

BASEDIR = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(str(BASEDIR/".."))

from main import app

class TestTemplates(unittest.TestCase):
	def test_templates(self):
		env = jinja2.Environment()
		templates = BASEDIR / ".." / "templates"
		for fname in os.listdir(templates):
			if os.path.isfile(fh := templates / fname):
				assert(env._parse(fh, fname, None))

	def test_sites(self):
		port = 5000
		with contextlib.redirect_stdout(out:=io.StringIO()), \
		     contextlib.redirect_stderr(err:=io.StringIO()):
			srv = threading.Thread(target=app.run, kwargs={"port":port}, daemon=True)
			srv.start()

			time.sleep(0.1)
			sites = requests.get(f"http://localhost:{port}/sitemap").json()
			tpool = []
			with ThreadPoolExecutor(8) as exec:
				for site in sites:
					tpool.append(exec.submit(
						requests.get, f"http://localhost:{port}{site}")
					)

			for task in as_completed(tpool):
				assert(task.result().ok)


if __name__ == "__main__":
	unittest.main()
