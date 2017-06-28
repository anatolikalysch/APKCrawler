from crawler import *


class eoemarket_crawler(two_way_crawler):
    def __init__(self):
        super().__init__('http://www.eoemarket.com/game/',
                         'http://www.eoemarket.com/soft/',
                         'http://www.eoemarket.com/game/2_hot_unofficial_hasad_2_2.html',
                         'http://www.eoemarket.com/soft/1_new_unofficial_hasad_1_2.html')
        self.folder_name = 'eoemarket/'
        self.baseUrl = 'http://www.eoemarket.com'
        if not os.path.exists(self.folder_name):
            os.mkdir(self.folder_name)

    def extraction_routine(self, string):
        if self.game:
            apps = re.findall(r'.*href="(/game/.*?\.html)".*', string)
        else:
            apps = re.findall(r'.*href="(/soft/.*?\.html)".*', string)

        for app in apps:
            try:
                apk_name = app.split('/')[-1].rstrip('/') + '.apk'
                if os.path.exists(self.folder_name + apk_name):
                    continue
                else:
                    website = requests.get(self.baseUrl + app, timeout=self.timeout, headers=self.header).text
                    dl_link = re.findall(r'href="(http://www.eoemarket.com/download/.*?)"', website)[0]

                    apk_bytes = requests.get(dl_link, allow_redirects=True, stream=True, timeout=self.timeout,
                                             headers=self.header)

                    with open(self.folder_name + apk_name, 'wb') as f:
                        for chunk in apk_bytes.iter_content(chunk_size=1024):
                            if chunk:  # filter out keep-alive new chunks
                                f.write(chunk)
            except Exception as e:
                pass

    def mutate_url(self, url, counter):
        if self.game:
            return 'http://www.eoemarket.com/game/2_hot_unofficial_hasad_2_{}.html'.format(counter)
        else:
            return 'http://www.eoemarket.com/soft/1_new_unofficial_hasad_1_{}.html'.format(counter)
