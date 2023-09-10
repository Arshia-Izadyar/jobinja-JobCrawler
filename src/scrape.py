import json
import re
import time

import requests
from bs4 import BeautifulSoup

import aiohttp
import asyncio


if __name__ == "__main__":
    headers = {'Authorization': 'barrer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJFbWFpbCI6ImFyc2hpYUBnbWFpbC5jb20iLCJFeHAiOjE2OTQzMjU2MTAsIkZ1bGxOYW1lIjoiVGVzdGxhc3QiLCJQaG9uZSI6IjA5MTA4NjI0NzA3IiwiUm9sZXMiOlsiYWRtaW4iXSwiVXNlcklkIjoxLCJVc2VyTmFtZSI6ImFkbWluIn0.8zFXyMw9sic6iambv3OTQSaeyNrvpSMOT-SPzEzg4E0'}
    res = requests.get("http://127.0.0.1:4000/api/v1/car-model/get/1", headers=headers)
    txt = res.text
    parsed = json.loads(txt)
    print(json.dumps(parsed, indent=4))
