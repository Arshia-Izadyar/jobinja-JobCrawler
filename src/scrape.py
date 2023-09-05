import re

from bs4 import BeautifulSoup
import requests
from requests.exceptions import Timeout, TooManyRedirects, ReadTimeout




def get_page(url):
    try:
        cookies = {
            "remember_82e5d2c56bdd0811318f0cf078b78bfc": "eyJpdiI6IlwvcE1MRGR3b0NrSUszQ0dobmlTRkZ3PT0iLCJ2YWx1ZSI6IkwySFpZUFJpdEtzQ0h5c0crVVd3RzR2R2hqaUFoQzdtZlBVZ3NlUVdMeFVmNUlHWVhzREZwbFU2NzN1UzFDVitmMkZqMEphUFYxWnpTWWhIaTcxZHYwSkFiSmFaeW1KT1wvWUpvMSs0VW9OQT0iLCJtYWMiOiJmYmRjMzQ2ZTMzZjhkODJhOGVjYjg0MmViODc4YmVlZmE2NmNlMzc4MzIxYmVhN2U1NDUyNGIwNjljYmQ0NzNiIn0%3D",
            "user_mode": "eyJpdiI6IlNlazg4RVwvanFVUm5FaENmVEVrc25RPT0iLCJ2YWx1ZSI6IjkwaDV5SDFhWlpRZlYwVHh3dXVRRVE9PSIsIm1hYyI6IjM4YWFhMzMxZWVlMTIwMzlhNTUyY2JjNWRmMzdjYTUxNTk5M2RiOWY2YTQzMzUwMmUxZTJiN2VjNTE3MGQxNDIifQ%3D%3D"
        }
        res = requests.get(url, cookies=cookies)

        res.raise_for_status()
        if res.status_code == 200:
            return res.text
        else:
            return None
    except (Timeout, TooManyRedirects, ReadTimeout) as e:
        print("error happened", e)


def scrape_page(url, page_count):
    result_data = []
    for i in range(1, page_count + 1):
        page_number = "&page={}"
        new_url = url + page_number.format(str(i))
        txt = get_page(new_url)
        soup = BeautifulSoup(txt, "html.parser")
        job_cards = soup.find_all("div", class_="c-jobListView__itemWrap")

        for job_card in job_cards:
            data = {}
            header = job_card.find("a", class_="c-jobListView__titleLink")
            title = header.text.strip()
            link = header.get("href")
            spans = job_card.find_all("span")
            days_passed = spans[0].text.strip()
            company = spans[1].text.strip()
            location = spans[2].text.strip()
            salary = re.sub(r'\s', "", spans[3].text.strip())
            data["title"] = title
            data["link"] = link
            data["days_passed"] = days_passed
            data["company"] = company
            data["location"] = location
            data["salary"] = salary
            result_data.append(data)
    return result_data

