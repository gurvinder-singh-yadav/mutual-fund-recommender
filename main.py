from src.scraper import *
from src.api_helper import *
import os
import pandas as pd
import datetime
        for path in paths:
            dfs.append(pd.read_csv(path, index_col=None))
            os.remove(path)
        df = pd.concat(dfs)
        os.rmdir(dir)
        df.to_csv(index_path, index=None)
    return "Done"
if __name__ == "__main__":
    # save_summaries()
    today = str(datetime.date.today())
    # concat("data/grow/{}/index".format(today))
    # scrape_funds()
    # concat_grow_funds()
    # get_tick_links()
    # get_tick_funds()
    # get_stock_urls()
    # concat_stock_urls()
    # get_stocks_info()
    # summarise_stocks()
    # get_stories(50)
    process_news()