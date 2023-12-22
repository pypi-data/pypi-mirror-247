# -*- coding: utf-8 -*-
import sys
import time
from pytrends.request import TrendReq
from pytrends.exceptions import TooManyRequestsError
import japanize_matplotlib
from matplotlib import pyplot as plt


def plot_trends(keywords):
    # pytrendsを初期化
    pytrends = TrendReq(hl='ja-JP', tz=360)
    try:
        pytrends.build_payload(keywords, cat=0, timeframe='now 7-d', geo='JP')
        data = pytrends.interest_over_time()
        for keyword in keywords:
            data[keyword].plot(label=keyword)
        plt.title('Google Trends for ' + ', '.join(keywords))
        plt.xlabel('Date')
        plt.ylabel('Trends Index')
        plt.grid(True)
        plt.legend()
        plt.savefig('result.png')
        plt.show()
    except TooManyRequestsError:
        print("リクエストが多すぎます。次のリクエストを行う前にしばらくお待ちください。")
        time.sleep(60)  # 60秒待つ

def main():
    if len(sys.argv) > 1:
        plot_trends(sys.argv[1:])
    else:
        print("Please provide at least one search query as a command line argument.")

if __name__ == "__main__":
    main()
