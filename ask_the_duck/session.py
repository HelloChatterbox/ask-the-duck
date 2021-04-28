import requests_cache
USER_AGENT = "ask_the_duck v0.0.1"
SESSION = requests_cache.CachedSession(expire_after=5 * 60, backend="memory")
SESSION.headers = {"User-Agent": USER_AGENT}