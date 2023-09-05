import requests
from bs4 import BeautifulSoup

li = {
    "developer": "وب،‌ برنامه‌نویسی و نرم‌افزار", "devops": "IT %2F DevOps %2F Server",
    "it": "IT %2F DevOps %2F Server", "sysAdmin": "IT %2F DevOps %2F Server",
    "marketing": "فروش و بازاریابی", "sale": "فروش و بازاریابی", "accounting": "مالی و حسابداری"
}

filter_dict = {
    "intern": "&filters[internship]={}",  # 1 for true 0 for false
    "remote": "&filters[remote]={}",  # 1 for true 0 for false
    "work_type": "&filters[job_types][1]={}",  # is_parttime or is_fulltime
    "time": "&preferred_before=1693922352&sort_by=relevance_desc",
    "category": "&filters[job_categories][]={}",
    "work_exp": "&filters[w_e][]={}",
    "title": "&filters[keywords][0]={}",
    "salary": "&filters[sal_min][2]={}%3A"
}
"""
intern      =>    &filters[internship]=1
remote      =>    &filters[remote]=1
part_time   =>    &filters[job_types][1]=is_parttime
full_time   =>    &filters[job_types][0]=is_fulltime
time        =>    &preferred_before=1693922352&sort_by=relevance_desc
title       =>    &filters[keywords][0]=node
cat         =>    &filters[job_categories][]=
work_exp    =>    &filters[w_e][]=under_two
work_exp    =>    &filters[w_e][]=3_6
work_exp    =>    &filters[w_e][]=7_plus
work_exp    =>    &filters[w_e][]=any
salary       =>    &filters[sal_min][2]= 5000000 / 10000000 / 20000000 / 35000000 / 50000000
"""


def configure_url(conf):
    base_link = "https://jobinja.ir/jobs?"
    base_link = work_category(base_link, conf["category"])
    base_link = is_full_time(base_link, conf["full_time"])
    base_link = is_intern(base_link, conf["is_intern"])
    base_link = is_remote(base_link, conf["is_remote"])
    base_link = add_salary(base_link, conf["salary"])

    if conf["work_exp"] is not None:
        base_link = work_expirence(base_link, conf["work_exp"])
    base_link = add_time_filter(base_link)

    return base_link


def work_category(base_link, cat: str):
    if cat in li:
        c = li[cat]
    else:
        c = "developer"
    return base_link + filter_dict["category"].format(c)


def work_expirence(base_link, work_years):
    if work_years == 0:
        return base_link + filter_dict["work_exp"].format("any")
    elif 2 >= work_years > 0:
        return base_link + filter_dict["work_exp"].format("under_two")
    elif 3 <= work_years <= 6:
        return base_link + filter_dict["work_exp"].format("3_6")
    else:
        return base_link + filter_dict["work_exp"].format("7_plus")


def is_full_time(base_link, full_time):
    if full_time is True:
        return base_link + filter_dict["work_type"].format("is_fulltime")
    else:
        return base_link + filter_dict["work_type"].format("is_parttime")


def is_intern(base_link, intern):
    if intern is True:
        return base_link + filter_dict["intern"].format("1")
    else:
        return base_link + filter_dict["intern"].format("0")


def is_remote(base_link, remote):
    if remote is True:
        return base_link + filter_dict["remote"].format("1")
    else:
        return base_link + filter_dict["remote"].format("0")


def add_salary(base_link, salary):
    if salary < 10_000_000:
        return base_link + filter_dict["salary"].format("4500000")
    elif 20_000_000 > salary >= 10_000_000:
        return base_link + filter_dict["salary"].format("10000000")
    elif salary >= 20_000_000:
        return base_link + filter_dict["salary"].format("35000000")

def add_time_filter(base_link):
    return base_link + filter_dict["time"]

conf = {"category": "developer", "full_time": True, "work_exp": 0, "is_intern": True, "is_remote": True,
        "salary": 30_000_000}

print(configure_url(conf))
