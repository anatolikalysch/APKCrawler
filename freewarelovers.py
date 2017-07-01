from crawler import *


class freewarelovers_crawler(crawler):
    def __init__(self):
        super().__init__('http://www.freewarelovers.com/android/apps', 'http://www.freewarelovers.com/android/apps')
        self.folder_name = 'freewarelovers/'
        self.baseUrl = 'http://www.freewarelovers.com'
        if not os.path.exists(self.folder_name):
            os.mkdir(self.folder_name)

    def start_crawl(self):
            try:
                self.extraction_routine(self.counter)
            except Exception as e:
                print(self.folder_name[:-1] + ': ' + str(e.args))

    def extraction_routine(self, ctr):
        startpage = requests.get('http://www.freewarelovers.com/android/apps', timeout=self.timeout, headers=self.header).text
        apps = re.findall(r'.*<ol>(.*?)</ol>.*', startpage)[0]
        sp = apps.split('href="')
        apps = [s.split('" title=')[0] for s in sp]
        for app in apps:
            try:
                apk_name = app.split('apps/')[1].rstrip('/') + '.apk'
                if os.path.exists(self.folder_name + apk_name):
                    pass
                else:
                    link = self.baseUrl + app
                    website = requests.get(link, timeout=self.timeout, headers=self.header).text
                    dl_link = re.findall(r'.*href="(/android/download/.*?\.apk)".*', website)[0]
                    apk_bytes = requests.get(self.baseUrl + dl_link, allow_redirects=True, stream=True, timeout=self.timeout,
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
