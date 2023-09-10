import time
import pandas as pd
from datetime import datetime


def export_csv(data):
    print("Creating CSV ...")
    time.sleep(1)
    df = pd.DataFrame(data)
    csv_file = "jobs_{}.csv".format(datetime.now().date())
    df.to_csv(csv_file, index=False)
    print("Done Create")
