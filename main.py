from src.scrape import scrape_page
from src.utils.url_configure import configure_url, work_fields
from src.utils.mongo import save_to_mongo, search_DB
import argparse
import asyncio

config = {
    "title": "",
    "full_time": True,
    "is_intern": False,
    "is_remote": False,
    "salary": None,
    "work_exp": 0,
    "category": ""
}

global Data


async def main():
    parser = argparse.ArgumentParser(description="this script will scrape the jobinja.ir")
    parser.add_argument("-s", "--scrape", help="enter how many pages should scrape 1-10 (it's exclusive)", type=int)
    parser.add_argument("-m", "--mongo", action="store_true", help="add items to mongo db")
    parser.add_argument("-c", "--csv", action="store_true", help="export to CSV")
    parser.add_argument("-f", "--find", help="enter the name of the job you want to search the data base", type=str)
    parser.add_argument("-t", "--tabel", help="enter the name of the tabel (title,category) comma separated", type=str)

    args = parser.parse_args()

    if args.scrape:
        category = str(input("Enter a Job category or type \"all\" to "
                             "see a list of supported category [default => (developer)]: ")).lower()

        if category != "" and category in work_fields.keys():
            config["category"] = category

        elif category == "all":
            for i in work_fields:
                print(f"category: {i} => {work_fields[i].replace('%2F', '').strip()}")
            quit()
        else:
            config["category"] = "developer"

        title = str(input("enter your preferred job title or empty for nil title [default => (any)]: ")).lower()
        config["title"] = title
        full_time = str(
            input("Type \"full\" for fullTime works or \"part\" for partTime [default => (FullTime)]: ")).lower()
        if full_time == "full":
            is_full_time = True
        elif full_time == "part":
            is_full_time = False
        else:
            is_full_time = True
        config["full_time"] = is_full_time

        intern_ship = str(
            input(
                "Type \"intern\" for internShip or leave blank for None internship [default => (None internship)]: ")).lower()
        if intern_ship == "intern":
            is_intern = True
        else:
            is_intern = False
        config["is_intern"] = is_intern

        remote = str(input(
            "Type \"remote\" for remote jobs works or leave blank for None remote jobs [default => (None remote)]: ")).lower()
        if remote == "remote":
            is_remote = True
        else:
            is_remote = False
        config["is_remote"] = is_remote

        salary = str(input("enter desired salary or leave blank [default => (any)]: "))
        if salary != "":
            config["salary"] = int(salary)

        work_exp = str(input("enter years of work experience [default => (any)]: "))
        if work_exp != "":
            config["work_exp"] = int(work_exp)
        else:
            config["work_exp"] = None
        link = configure_url(config)
        print(f"generated link:\n{link}")
        Data = await scrape_page(link, args.scrape)
    if args.csv:
        pass
    if args.mongo:
        print("started To save data to mongoDB ... ")
        save_to_mongo(Data, "title_" + config["title"] + "_cat-" + config["category"])
    elif args.find and args.tabel:
        tabel = args.tabel.split(",")
        result = search_DB(args.find, "title_" + tabel[0] + "_cat-" + tabel[1])
        for res in result:
            print(res)
            print()

if __name__ == "__main__":
    asyncio.run(main())
