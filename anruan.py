from crawler import *


class anruan_crawler(two_way_crawler):
    def __init__(self):
        super().__init__('http://game.anruan.com/index_1.html',
                         'http://soft.anruan.com/index_1.html',
                         'http://game.anruan.com/index_1.html',
                         'http://soft.anruan.com/index_1.html')
        self.folder_name = 'anruan/'
        if not os.path.exists(self.folder_name):
            os.mkdir(self.folder_name)

    def extraction_routine(self, string):
        if self.game:
            apps = re.findall(r'.*href="(http://game.anruan.com/g-.*?/)".*', string)
        else:
            apps = re.findall(r'.*href="(http://soft.anruan.com/.*?/)".*', string)

        for app in apps:
            try:
                apk_name = app.split('.com/')[1].rstrip('/') + '.apk'
                if os.path.exists(self.folder_name + apk_name):
                    continue
                else:
                    website = requests.get(app, timeout=self.timeout, headers=self.header).text
                    if self.game:
                        dl_link = re.findall(r'href="(http://game.anruan.com/gdown.php\?id=.*?)"', website)[0]
                    else:
                        dl_link = re.findall(r'href="(http://soft.anruan.com/down.php\?id=.*?)"', website)[0]
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

    def mutate_url(self, url, counter):
        split = url.split('.com')
        result = split[0] + '.com/index_{}.html'.format(counter)
        return result
