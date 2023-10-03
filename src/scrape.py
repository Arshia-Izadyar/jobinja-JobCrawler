import re
import time

from bs4 import BeautifulSoup

import aiohttp
import asyncio


async def get_page(url):
    cookies = {
        "remember_82e5d2c56bdd0811318f0cf078b78bfc": "eyJpdiI6IlwvcE1MRGR3b0NrSUszQ0dobmlTRkZ3PT0iLCJ2YWx1ZSI6IkwySFpZUFJpdEtzQ0h5c0crVVd3RzR2R2hqaUFoQzdtZlBVZ3NlUVdMeFVmNUlHWVhzREZwbFU2NzN1UzFDVitmMkZqMEphUFYxWnpTWWhIaTcxZHYwSkFiSmFaeW1KT1wvWUpvMSs0VW9OQT0iLCJtYWMiOiJmYmRjMzQ2ZTMzZjhkODJhOGVjYjg0MmViODc4YmVlZmE2NmNlMzc4MzIxYmVhN2U1NDUyNGIwNjljYmQ0NzNiIn0%3D",
        "user_mode": "eyJpdiI6IlNlazg4RVwvanFVUm5FaENmVEVrc25RPT0iLCJ2YWx1ZSI6IjkwaDV5SDFhWlpRZlYwVHh3dXVRRVE9PSIsIm1hYyI6IjM4YWFhMzMxZWVlMTIwMzlhNTUyY2JjNWRmMzdjYTUxNTk5M2RiOWY2YTQzMzUwMmUxZTJiN2VjNTE3MGQxNDIifQ%3D%3D"
    }
    try:
        async with aiohttp.ClientSession(cookies=cookies) as session:
            async with session.get(url) as response:
                response.raise_for_status()
                if response.status == 200:
                    return await response.text()
                else:
                    return None
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        print("Error happened:", e)


async def scrape_page(url, page_count):
    start_time = time.time()
    result_data = []
    for i in range(1, page_count + 1):
        print(f"scraping for page number {i} started")
        page_number = "&page={}"
        new_url = url + page_number.format(str(i))
        txt = await get_page(new_url)
        soup = BeautifulSoup(txt, "html.parser")
        job_cards = soup.find_all("div", class_="c-jobListView__itemWrap")
        if len(job_cards) == 0:
            break

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
    end_time = time.time()

    # Calculate the runtime in seconds
    runtime = end_time - start_time
    s_counter = 0
    for j in result_data:
        if "senior" in j["title"] or "ارشد" in j["title"]:
            s_counter += 1
    if len(result_data) != 0:
        p1 = (s_counter / len(result_data)) * 100
        p1 = round(p1, 2)
        p2 = 100 - p1
    res = f"Found {len(result_data)} jobs in {round(runtime, 2)}\nin total {p1}% of jobs want senior and {round(p2, 2)}% none Senior"
    print(res)
    return result_data