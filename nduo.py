from crawler import *


class nduo_crawler(crawler):
    def __init__(self):
        super().__init__('http://www.nduo.cn/', 'http://market2.nduoa.com/softs.ashx?act=207&resId=984216')
        self.folder_name = 'nduo/'
        if not os.path.exists(self.folder_name):
            os.mkdir(self.folder_name)

    def start_crawl(self):
        while True:
            try:
                self.extraction_routine(self.counter)
                self.counter += 1
            except Exception as e:
                break

    def extraction_routine(self, ctr):
        apk_name = 'nduo' + str(ctr) + '.apk'
        try:
            if os.path.exists(self.folder_name + apk_name):
                pass
            else:
                link = 'http://market2.nduoa.com/softs.ashx?act=207&resId=9%05d' % ctr
                apk_bytes = requests.get(link, allow_redirects=True, stream=True, timeout=self.timeout,
                                         headers=self.header)

                with open(self.folder_name + apk_name, 'wb') as f:
                    for chunk in apk_bytes.iter_content(chunk_size=1024):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
        except:
            pass
