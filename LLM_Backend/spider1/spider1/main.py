from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from threading import Thread
from spiders.bksy import BksySpider
from spiders.ckc import CkcSpider
from spiders.danqing import DQXYSpider
from spiders.jiaoliu import UgrsSpider
from spiders.lantian import LantianSpider
from spiders.yunfeng import YunfengSpider
from spiders.qiushi import QsxySpider
from spiders.kyjs import run_kyjs_crawler

import os
import json
import pandas as pd

def run_scrapy_crawlers():
    runner = CrawlerRunner(settings={
        "LOG_LEVEL": "INFO",  # 设置日志级别
    })

    # 添加所有爬虫到CrawlerRunner
    d = runner.crawl(BksySpider)
    d.addBoth(lambda _: runner.crawl(CkcSpider))
    d.addBoth(lambda _: runner.crawl(DQXYSpider))
    d.addBoth(lambda _: runner.crawl(UgrsSpider))
    d.addBoth(lambda _: runner.crawl(LantianSpider))
    d.addBoth(lambda _: runner.crawl(QsxySpider))
    d.addBoth(lambda _: runner.crawl(YunfengSpider))

    # 启动所有爬虫
    d.addBoth(lambda _: reactor.stop())
    reactor.run()

def main():
    # 运行kyjs.py脚本
    run_kyjs_crawler()

    # 运行Scrapy爬虫
    run_scrapy_crawlers()
    # 示例调用
    # result_folder = './result'
    # target_txt = './ragtest/input/input.txt'
    # df = merge_json_to_dataframe(result_folder)
    # save_dataframe_to_txt(df, target_txt)

if __name__ == "__main__":
    main()

def merge_json_to_dataframe(result_folder):
    # 创建一个空的 DataFrame 列表来存储所有数据
    data_frames = []

    if not os.path.exists(result_folder):
        raise FileNotFoundError(f"The result folder '{result_folder}' does not exist.")

    for root, dirs, files in os.walk(result_folder):
        for dir in dirs:
            sub_folder = os.path.join(root, dir)
            for sub_root, _, sub_files in os.walk(sub_folder):
                for file in sub_files:
                    if file.endswith('.json'):
                        json_path = os.path.join(sub_root, file)
                        try:
                            with open(json_path, 'r', encoding='utf-8') as json_file:
                                data = json.load(json_file)
                                # 如果是字典类型数据，检查 content 和 title 字段并处理
                                if isinstance(data, dict):
                                    if data.get('content') and data['content'].strip() != '' and \
                                       data.get('title') and '公示名单' not in data['title'] and \
                                       '名单公示' not in data['title'] and \
                                       '发展党员情况公示' not in data['title'] and \
                                       '值班安排' not in data['title'] and \
                                       '委培生名单' not in data['title'] and \
                                       '交换生名单' not in data['title']:
                                        data_frames.append(pd.DataFrame([data]))
                                elif isinstance(data, list):
                                    for item in data:
                                        if isinstance(item, dict) and item.get('content') and item['content'].strip() != '' and \
                                           item.get('title') and '公示名单' not in item['title'] and \
                                           '名单公示' not in data['title'] and \
                                           '发展党员情况公示' not in data['title'] and \
                                           '值班安排' not in item['title'] and \
                                           '委培生名单' not in item['title'] and \
                                           '交换生名单' not in item['title']:
                                            data_frames.append(pd.DataFrame([item]))
                        except json.JSONDecodeError as e:
                            print(f"Error decoding JSON from file {json_path}: {e}")
                        except Exception as e:
                            print(f"An error occurred while processing file {json_path}: {e}")

    # 合并所有 DataFrame
    if data_frames:
        combined_df = pd.concat(data_frames, ignore_index=True)
    else:
        combined_df = pd.DataFrame()  # 如果没有数据，返回一个空 DataFrame

    return combined_df

def save_dataframe_to_txt(df, target_txt):
    # 保存 DataFrame 为文本格式，每行一个 JSON 字符串
    df.to_json(target_txt, orient='records', lines=True, force_ascii=False)
