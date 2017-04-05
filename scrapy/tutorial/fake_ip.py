from stem import Signal
from stem.control import Controller
import requests
import urllib


def set_new_ip():
    """Change IP using TOR"""
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password='tor_password')
        controller.signal(Signal.NEWNYM)

def download(ip_set, url, file_name):
    set_new_ip()
    r = requests.get(url='http://icanhazip.com/',
                          proxies=http_proxy,
                          verify=False)
    ip = r.text

    while ip in ip_set:
        set_new_ip()
        ip = requests.get(url='http://icanhazip.com/',
                          proxies=http_proxy,
                          verify=False).text
    print ip
    try:
        r = requests.get(url, proxies=http_proxy, verify=False)
        print r.status_code
        while r.status_code != 200:
            r = requests.get(url, proxies=http_proxy, verify=False)
        ip_set.add(ip)
        with open(file_name, 'wb') as fh:
            fh.write(r.content)
    except:
        print 'download fails for PDF ' + file_name


local_proxy = 'http://127.0.0.1:8118'
http_proxy = {'http': local_proxy,
              'https': local_proxy}

# current_ip = requests.get(url='http://icanhazip.com/',
#                           proxies=http_proxy,
#                           verify=False)
# print type(current_ip)
# print current_ip.text
ip_set = set()
id_set = set()

id_fh = open('id_list.txt', 'r')
for line in id_fh:
    id_set.add(line.strip())

print id_set

for pdf_id in id_set:
    download(ip_set, 'http://fcst.ceaj.org/CN/article/downloadArticleFile.do?attachType=PDF&id=' + pdf_id, './tor/' + pdf_id + '.pdf')
