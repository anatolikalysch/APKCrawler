from crawler import *


class shoujibaidu_crawler(crawler):
    def __init__(self):
        super().__init__('http://shouji.baidu.com/software/', 'http://shouji.baidu.com/software/10000001.html')
        self.folder_name = 'baidu/'
        if not os.path.exists(self.folder_name):
            os.mkdir(self.folder_name)

    def start_crawl(self):
        while True:
            try:
                self.extraction_routine(self.counter)
                self.counter += 1
            except Exception as e:
                print(self.folder_name[:-1] + ': ' + str(e.args))
                break

    def extraction_routine(self, ctr):
        apk_name = 'baidu' + str(ctr) + '.apk'
        try:
            if os.path.exists(self.folder_name + apk_name):
                pass
            else:
                link = 'http://shouji.baidu.com/software/1%07d.html' % ctr
                website = requests.get(link, timeout=self.timeout, headers=self.header).text
                dl_link = re.findall(r'.*href="(http://p.gdown.baidu.com/.*?)".*', website)[0]
                apk_bytes = requests.get(dl_link, allow_redirects=True, stream=True, timeout=self.timeout,
                                         headers=self.header)

                if apk_bytes.status_code != 200:
                    pass
                else:
                    with open(self.folder_name + apk_name, 'wb') as f:
                        for chunk in apk_bytes.iter_content(chunk_size=1024):
                            if chunk:  # filter out keep-alive new chunks
                                f.write(chunk)
        except Exception as e:
            print(self.folder_name[:-1] + ': ' + str(e.args))
