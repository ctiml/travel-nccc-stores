from pyquery import PyQuery as pq
import urllib.request
import urllib.parse
import re


def fetch_page(url):
    resp = None
    retry = 5
    while True:
        try:
            resp = urllib.request.urlopen(url)
            break
        except Exception as e:
            print(e)
            retry -= 1
            if retry == 0:
                break
    return resp


def main():
    page = 1
    count = 1000

    host = 'http://travel.nccc.com.tw'
    path = '/NASApp/NTC/servlet/com.du.mvc.EntryServlet'
    params = {
        'Action': 'RetailerList',
        'Type': 'GetFull',
        'WebMode': 'text',
        'Request': 'NULL_NULL_NULL_NULL_NULL_NULL_NULL_NULL_NULL_0_{0}_{1}_0'
    }
    param_str = '&'.join('%s=%s' % (k, v) for k, v in params.items())
    url_template = host + path + '?' + param_str

    f = open('ids', 'w')

    while True:
        print('Page: {0}'.format(page))
        url = url_template.format(page, count)
        resp = fetch_page(url)
        if resp is None:
            exit()
        d = pq(resp.read())
        links = d('table table table table td[align=center] a')
        if links.size() == 0:
            break

        for link in links:
            # import code; code.interact(local=locals())
            if link.text != '詳細內容':
                continue
            m = re.search('Id=(\d+)', link.attrib['href'])
            detail_id = m.group(1)
            f.write(detail_id + "\n")
        page += 1

if __name__ == "__main__":
    main()
