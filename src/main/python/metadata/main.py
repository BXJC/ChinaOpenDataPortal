import json
import time
import urllib

from constants import (METADATA_SAVE_PATH, PROVINCE_CURL_JSON_PATH, PROVINCE_LIST)
from detail import Detail
from resultlist import ResultList

curls = {}


class Crawler:
    def __init__(self, province, city):
        self.province = province
        self.city = city
        self.result_list = ResultList(self.province, self.city)
        self.detail = Detail(self.province, self.city)
        self.result_list_curl = curls[province][city]['resultList']
        self.detail_list_curl = curls[province][city]['detail']
        self.metadata_list = []

    def crawl(self):
        func_name = f"crawl_{str(self.province)}_{str(self.city)}"
        func = getattr(self, func_name, self.crawl_other)
        func()

    # TODO: 反爬虫 ConnectionResetError: [WinError 10054]
    def crawl_beijing_beijing(self):
        for page in range(1, 2):
            print(page)
            curl = self.result_list_curl.copy()
            curl['data']['curPage'] = str(page)
            links = self.result_list.get_result_list(curl)
            for link in links:
                curl = self.detail_list_curl.copy()
                curl['url'] = link
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_tianjin_tianjin(self):
        curl = self.result_list_curl.copy()
        links = self.result_list.get_result_list(curl)
        for link in links[:10]:
            curl = self.detail_list_curl.copy()
            curl['url'] = link
            metadata = self.detail.get_detail(curl)
            print(metadata)
            self.metadata_list.append(metadata)

    def crawl_hebei_hebei(self):
        for page in range(1, 5):
            print(page)
            curl = self.result_list_curl.copy()
            curl['data']['pageNo'] = str(page)
            metadata_ids = self.result_list.get_result_list(curl)
            for metadata_id in metadata_ids:
                curl = self.detail_list_curl.copy()
                curl['data']['rowkey'] = metadata_id['METADATA_ID']
                curl['data']['list_url'] = curl['data']['list_url'].format(page)
                metadata = self.detail.get_detail(curl)
                metadata['所属主题'] = metadata_id['THEME_NAME']
                metadata['发布时间'] = metadata_id['CREAT_DATE']
                metadata['更新日期'] = metadata_id['UPDATE_DATE']
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_neimenggu_neimenggu(self):
        for page in range(1, 5):
            print(page)
            curl = self.result_list_curl.copy()
            curl['data']['page'] = str(page)
            ids = self.result_list.get_result_list(curl)
            for id in ids:
                curl = self.detail_list_curl.copy()
                curl['data']['id'] = id
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_liaoning_liaoning(self):
        for page in range(1, 26):
            print(page)
            curl = self.result_list_curl.copy()
            curl['queries']['page'] = str(page)
            links = self.result_list.get_result_list(curl)
            for link in links:
                curl = self.detail_list_curl.copy()
                curl['url'] += link
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_liaoning_shenyang(self):
        for page in range(1, 202):
            print(page)
            curl = self.result_list_curl.copy()
            curl['queries']['page'] = str(page)
            links = self.result_list.get_result_list(curl)
            for link in links:
                curl = self.detail_list_curl.copy()
                curl['url'] += link
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_heilongjiang_harbin(self):
        for page in range(1, 295):
            print(page)
            curl = self.result_list_curl.copy()
            curl['queries']['page'] = str(page)
            links = self.result_list.get_result_list(curl)
            for link in links:
                curl = self.detail_list_curl.copy()
                curl['url'] += link
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_jilin_jilin(self):
        for page in range(1, 25):
            print(page)
            curl = self.result_list_curl.copy()
            curl['data']['page'] = str(page)
            links = self.result_list.get_result_list(curl)
            for link in links:
                curl = self.detail_list_curl.copy()
                curl['url'] += link
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_shandong_shandong(self):
        for page in range(1, 5):
            print(page)
            curl = self.result_list_curl.copy()
            curl['params']['page'] = str(page)
            links = self.result_list.get_result_list(curl)
            for link in links:
                curl = self.detail_list_curl.copy()
                curl['url'] += link
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_jiangsu_jiangsu(self):
        for city in ['', 'all']:
            for page in range(0, 10):
                print(page)
                curl = self.result_list_curl.copy()
                curl['data'] = curl['data'].format(page, city)
                rowGuids = self.result_list.get_result_list(curl)
                for rowGuid in rowGuids:
                    curl = self.detail_list_curl.copy()
                    curl['url'] = curl['url'].format(rowGuid)
                    curl['data'] = curl['data'].format(rowGuid)
                    metadata = self.detail.get_detail(curl)
                    print(metadata)
                    self.metadata_list.append(metadata)

    def crawl_shanghai_shanghai(self):
        for page in range(1, 5):
            print(page)
            curl = self.result_list_curl.copy()
            curl['data'] = curl['data'].replace('\"pageNum\":1', f'\"pageNum\":{page}').encode()
            dataset_ids = self.result_list.get_result_list(curl)
            for dataset_id in dataset_ids:
                curl = self.detail_list_curl.copy()
                curl['headers']['Referer'] = curl['headers']['Referer'].format(
                    dataset_id['datasetId'], urllib.parse.quote(dataset_id['datasetName']))
                curl['url'] = curl['url'].format(dataset_id['datasetId'])
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_zhejiang_zhejiang(self):
        for page in range(1, 5):
            print(page)
            curl = self.result_list_curl.copy()
            curl['data']['pageNumber'] = str(page)
            iids = self.result_list.get_result_list(curl)
            for iid in iids:
                curl = self.detail_list_curl.copy()
                curl['queries'] = iid
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_anhui_anhui(self):
        for page in range(1, 100000000):
            print(page)
            curl = self.result_list_curl.copy()
            curl['data']['pageNum'] = str(page)
            rids = self.result_list.get_result_list(curl)
            if len(rids) == 0:
                break
            for rid in rids:
                curl = self.detail_list_curl.copy()
                curl['headers']['Referer'] = curl['headers']['Referer'].format(rid)
                curl['data']['rid'] = rid
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_anhui_hefei(self):
        for page in range(1, 5):
            print(page)
            curl = self.result_list_curl.copy()
            curl['queries']['currentPageNo'] = str(page)
            curl['queries']['_'] = str(int(round(time.time() * 1000)))
            curl['headers']['Referer'] = curl['headers']['Referer'].format(str(page))
            ids = self.result_list.get_result_list(curl)
            if len(ids) == 0:
                break
            for id in ids:
                curl = self.detail_list_curl.copy()
                curl['data']['id'] = id
                curl['data']['zyId'] = id
                curl['headers']['Referer'] = curl['headers']['Referer'].format(str(page), id, id)
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_anhui_wuhu(self):
        for page in range(1, 5):
            print(page)
            curl = self.result_list_curl.copy()
            curl['data']['pageNo'] = str(page)
            ids = self.result_list.get_result_list(curl)
            if len(ids) == 0:
                break
            for id in ids:
                curl = self.detail_list_curl.copy()
                curl['headers']['Referer'] = curl['headers']['Referer'].format(str(page), id, id)
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_anhui_suzhou(self):
        for page in range(1, 54):
            print(page)
            curl = self.result_list_curl.copy()
            curl['queries']['page'] = str(page)
            links = self.result_list.get_result_list(curl)
            if len(links) == 0:
                break
            for link in links:
                curl = self.detail_list_curl.copy()
                curl['url'] += link['link']
                metadata = self.detail.get_detail(curl)
                metadata['数据格式'] = link['data_formats']
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_anhui_chizhou(self):
        for page in range(1, 276):
            print(page)
            curl = self.result_list_curl.copy()
            curl['queries']['page'] = str(page)
            metadatas = self.result_list.get_result_list(curl)
            if len(metadatas) == 0:
                break
            for metadata in metadatas:
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_jiangxi_jiangxi(self):
        for page in range(1, 5):
            print(page)
            curl = self.result_list_curl.copy()
            curl['data']['current'] = page
            data_ids = self.result_list.get_result_list(curl)
            for data_id in data_ids:
                curl = self.detail_list_curl.copy()
                curl['headers']['Referer'] = curl['headers']['Referer'].format(data_id)
                curl['queries']['dataId'] = data_id
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_fujian_fujian(self):
        for page in range(1, 5):
            print(page)
            curl = self.result_list_curl.copy()
            curl['queries']['page'] = str(page)
            links = self.result_list.get_result_list(curl)
            for link in links:
                curl = self.detail_list_curl.copy()
                curl['url'] += link
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_guangdong_guangdong(self):
        for page in range(1, 5):
            print(page)
            curl = self.result_list_curl.copy()
            curl['data']['pageNo'] = page
            res_ids = self.result_list.get_result_list(curl)
            for res_id in res_ids:
                curl = self.detail_list_curl.copy()
                curl['data']['resId'] = res_id
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_guangxi_guangxi(self):
        for page in range(1, 5):
            print(page)
            curl = self.result_list_curl.copy()
            curl['queries']['page'] = str(page)
            links = self.result_list.get_result_list(curl)
            for link in links:
                curl = self.detail_list_curl.copy()
                curl['url'] += link
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_hainan_hainan(self):
        for page in range(0, 5):
            print(page)
            curl = self.result_list_curl.copy()
            curl['data']['curPage'] = page
            ids = self.result_list.get_result_list(curl)
            for id in ids:
                curl = self.detail_list_curl.copy()
                curl['url'] = curl['url'].format(id)
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_ningxia_ningxia(self):
        for page in range(1, 5):
            print(page)
            curl = self.result_list_curl.copy()
            curl['queries']['page'] = str(page)
            links = self.result_list.get_result_list(curl)
            for link in links:
                curl = self.detail_list_curl.copy()
                curl['url'] += link
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_shaanxi_shaanxi(self):
        for page in range(1, 5):
            print(page)
            curl = self.result_list_curl.copy()
            curl['queries']['page.pageNo'] = str(page)
            ids = self.result_list.get_result_list(curl)
            for id in ids:
                curl = self.detail_list_curl.copy()
                curl['queries']['id'] = str(id)
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_sichuan_sichuan(self):
        for page in range(1, 5):
            print(page)
            curl = self.result_list_curl.copy()
            curl['queries']['page'] = str(page)
            links = self.result_list.get_result_list(curl)
            for link in links:
                curl = self.detail_list_curl.copy()
                curl['url'] += link
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_guizhou_guizhou(self):
        for page in range(1, 5):
            print(page)
            curl = self.result_list_curl.copy()
            curl['data']['pageIndex'] = page
            ids = self.result_list.get_result_list(curl)
            for id in ids:
                curl = self.detail_list_curl.copy()
                curl['data']['id'] = id
                metadata = self.detail.get_detail(curl)
                print(metadata)
                self.metadata_list.append(metadata)

    def crawl_other(self):
        print("暂无该省")

    def save_matadata_as_json(self, save_dir):
        filename = save_dir + self.province + '_' + self.city + '.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.metadata_list, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    provinces = PROVINCE_LIST
    with open(PROVINCE_CURL_JSON_PATH, 'r', encoding='utf-8') as curlFile:
        curls = json.load(curlFile)

    crawler = Crawler("heilongjiang", "harbin")
    crawler.crawl()
    crawler.save_matadata_as_json(METADATA_SAVE_PATH)
    # for province in provinces:
    #     crawler = Crawler(province)
    #     crawler.crawl()
