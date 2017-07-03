from crawler import *

class up2down_crawler(crawler):
    def __init__(self):
        super().__init__('https://en.uptodown.com/android/newreleases',
                         'https://en.uptodown.com/android/newreleases/')
        self.urlBase = 'https://en.uptodown.com'
        self.folder_name = 'up2down/'
        if not os.path.exists(self.folder_name):
            os.mkdir(self.folder_name)

    def mutate_url(self, url, counter):
        result = self.template + '{}'.format(self.counter)
        return result

    def extraction_routine(self, string):
        apps = re.findall(r'.*href="(http.*?en.uptodown.com/android)".*', string)
        for app in apps:
            try:
                app_website = requests.get(app, timeout=self.timeout, headers=self.header).text
                dl_link = re.findall(
                    r'.*href="(http.*?\.en\.uptodown\.com/android/download)".*',
                    app_website)[0]
                apk_name = dl_link.split('.en.')[0].lstrip('https://') + '.apk'
                no_app = requests.get(dl_link, allow_redirects=True, stream=True,
                                             timeout=self.timeout, headers=self.header).text
                dl_link = re.findall(r'.*href="(http.*?uptodown\.com/dwn/.*?)"', no_app)[0]
                if os.path.exists(self.folder_name + apk_name):
                    continue
                else:
                    apk_bytes = requests.get(dl_link, allow_redirects=True, stream=True,
                                             timeout=self.timeout, headers=self.header)

                    with open(self.folder_name + apk_name, 'wb') as f:
                        for chunk in apk_bytes.iter_content(chunk_size=1024):
                            if chunk:  # filter out keep-alive new chunks
                                f.write(chunk)
            except Exception as e:
                print(self.folder_name[:-1] + ': ' + str(e.args))
