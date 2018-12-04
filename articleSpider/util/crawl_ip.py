import requests
from scrapy.selector import Selector
import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', password='yjh961024', db='spider', charset='utf8')
cursor = conn.cursor()


def crawl_ips():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
    for i in range(3000):
        response = requests.get('http://www.xicidaili.com/nn/{0}'.format(i), headers=headers)
        selector = Selector(response.text)
        all_trs = selector.css('#ip_list tr')
        ip_list = []
        for tr in all_trs:
            speed_str = tr.css('.bar::attr("title")').extract_first()
            speed = 0
            if speed_str:
                speed = float(speed_str.split('秒')[0])
            all_text = tr.css('td::text').extract()
            ip = all_text[0]
            port = all_text[1]

            ip_list.append((ip, port, speed))

        for ip_info in ip_list:
            cursor.execute(
                'insert into proxy_ip values("{0}", "{1}", "{2}")'.format(
                    ip_info[0], ip_info[1], ip_info[2]
                )
            )
            conn.commit()


class GetIP(object):

    def delete_ip(self, ip):
        delete_sql = """
            delete from proxy_ip where ip='{0}'
        """.format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def judge_ip(self, ip, port):
        http_url = "http://www.baidu.com"
        proxy_url = "http://{0}:{1}".format(ip, port)
        try:
            proxy_dict = {
                "http": proxy_url,
            }
            response = requests.get(http_url, proxies=proxy_dict)
        except Exception as e:
            print("invalid ip and port")
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if 200 <= code < 300:
                print("effective ip")
                return True
            else:
                print("invalid ip and port")
                self.delete_ip(ip)
                return False

    def get_random_ip(self):
        random_sql = """
              SELECT ip, port FROM proxy_ip
            ORDER BY RAND()
            LIMIT 1
            """
        cursor.execute(random_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]

            judge_re = self.judge_ip(ip, port)
            if judge_re:
                return "http://{0}:{1}".format(ip, port)
            else:
                return self.get_random_ip()
