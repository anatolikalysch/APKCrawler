from crawler import *


class ONEappmarket_crawler(crawler):
    def __init__(self):
        super().__init__('http://www.1appmarket.com/developerapps.php?type=developers&cat=&page=1',
                         'http://www.1appmarket.com/developerapps.php?type=developers&cat=&page=')
        self.urlBase = 'http://www.1appmarket.com'
        self.folder_name = '1appmarket/'
        if not os.path.exists(self.folder_name):
            os.mkdir(self.folder_name)

    def mutate_url(self, url, counter):
        result = self.template + '{}'.format(self.counter)
        return result

    def extraction_routine(self, string):
        apps = re.findall(r'.*href="(/developers/.*?)".*', string)
        for app in apps:
            try:
                apk_name = app.split('/')[-1] + '.apk'
                if os.path.exists(self.folder_name + apk_name):
                    continue
                else:
                    app_website = requests.get(self.baseUrl + app, timeout=self.timeout, headers=self.header).text
                    dl_link = re.findall(
                        r'.*(http://www.1appmarket.com/.*?\.apk).*',
                        app_website)[0]

                    apk_bytes = requests.get(dl_link, allow_redirects=True, stream=True,
                                             timeout=self.timeout, headers=self.header)

                    with open(self.folder_name + apk_name, 'wb') as f:
                        for chunk in apk_bytes.iter_content(chunk_size=1024):
                            if chunk:  # filter out keep-alive new chunks
                                f.write(chunk)
            except Exception as e:
                print(self.folder_name[:-1] + ': ' + str(e.args))
