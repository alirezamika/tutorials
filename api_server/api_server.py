from autoscraper import AutoScraper
from flask import Flask, request


ebay_scraper = AutoScraper()
etsy_scraper = AutoScraper()
ebay_scraper.load('ebay-search')
etsy_scraper.load('etsy-search')
app = Flask(__name__)


def get_ebay_result(search_query):
    url = 'https://www.ebay.com/sch/i.html?_nkw=%s' % search_query
    result = ebay_scraper.get_result_similar(url, group_by_alias=True)
    return _aggregate_result(result)


def get_etsy_result(search_query):
    url = 'https://www.etsy.com/search?q=%s' % search_query
    result = etsy_scraper.get_result_similar(url, group_by_alias=True)
    result['url'] = [f'https://www.etsy.com/listing/{i}' for i in result['url']]
    return _aggregate_result(result)


def _aggregate_result(result):
    final_result = []
    for i in range(len(list(result.values())[0])):
        final_result.append({alias: result[alias][i] for alias in result})
    return final_result


@app.route('/', methods=['GET'])
def search_api():
    query = request.args.get('q')
    return dict(result=get_ebay_result(query) + get_etsy_result(query))


if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')

