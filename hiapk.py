from crawler import *


class hiapk_crawler(two_way_crawler):
    def __init__(self):
        super().__init__('http://apk.hiapk.com/games',
                         'http://apk.hiapk.com/apps',
                         'http://apk.hiapk.com/games?sort=5&pi=2',
                         'http://apk.hiapk.com/apps?sort=5&pi=2')
        self.folder_name = 'hiapk/'
        self.timeout = 30
        if not os.path.exists(self.folder_name):
            os.mkdir(self.folder_name)

    def extraction_routine(self, string):
        apps = re.findall(r'.*href="(/appdown/.*?)".*', string)
        for app in apps:
            try:
                apk_name = app.split('down/')[1].rstrip('/') + '.apk'
                if os.path.exists(self.folder_name + apk_name):
                    pass
                else:
                    if self.game:
                        apk_bytes = requests.get(self.baseGameUrl + app + '/', allow_redirects=True, stream=True,
                                                 timeout=self.timeout, headers=self.header)
                    else:
                        apk_bytes = requests.get(self.baseSoftUrl + app + '/', allow_redirects=True, stream=True,
                                                 timeout=self.timeout, headers=self.header)

                    if apk_bytes.status_code != 200:
                        pass
                    else:
                        with open(self.folder_name + apk_name, 'wb') as f:
                            for chunk in apk_bytes.iter_content(chunk_size=1024):
                                if chunk:  # filter out keep-alive new chunks
                                    f.write(chunk)
            except Exception as e:
                print(self.folder_name[:-1] + ': ' + str(e.args))

    def mutate_url(self, url, counter):
        if self.game:
            return 'http://apk.hiapk.com/games?sort=5&pi={}'.format(counter)
        else:
            return 'http://apk.hiapk.com/apps?sort=5&pi={}'.format(counter)
