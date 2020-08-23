from urllib.parse import urlparse
from urllib.parse import parse_qs


parsed = urlparse(url)
print(parse_qs(parsed.query))