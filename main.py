
import json
from src.scrapper import Grow




if __name__ == "__main__":
    grow = Grow()
    grow.funds_url(n=27)
    grow.get_fund_distribution()
    with open("data/file.txt", 'w') as f:
        json.dump(grow.funds, f)