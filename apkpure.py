from crawler import *


class apkpure_crawler(two_way_crawler):
    def __init__(self):
        super().__init__('https://apkpure.com/game',
                         'https://apkpure.com/app',
                         'https://apkpure.com/game?page=2',
                         'https://apkpure.com/app?page=2')
        self.folder_name = 'apkpure/'
        self.baseUrl = 'https://apkpure.com'
        if not os.path.exists(self.folder_name):
            os.mkdir(self.folder_name)

    def extraction_routine(self, string):
        apps = re.findall(r'.*href="(/.*?/download\?from=category)".*', string)

        for app in apps:
            try:
                apk_name = app.split('download')[0].split('/')[1].strip('/') + '.apk'
                if os.path.exists(self.folder_name + apk_name):
                    continue
                else:
                    website = requests.get(self.baseUrl + app, timeout=self.timeout, headers=self.header).text
                    dl_link = re.findall(r'href="(https://download.apkpure.com/.*?)">click.*', website)[0]

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
        return url.split('?')[0] + '?page={}'.format(counter)
