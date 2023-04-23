from src.scraper import save_summaries
import os
import pandas as pd
import datetime
def concat(dir):
    paths = os.listdir(dir)
    dfs = []
    # print(paths)
    if len(paths) > 1:
        for path in paths:
            path = os.path.join(dir, path)
            dfs.append(pd.read_csv(path, index_col=None))
            os.remove(path)
        df = pd.concat(dfs)
        df.to_csv(os.path.join(dir, "index.csv"), index=None)
if __name__ == "__main__":
    save_summaries()
    today = str(datetime.date.today())
    concat("data/grow/{}/index".format(today))