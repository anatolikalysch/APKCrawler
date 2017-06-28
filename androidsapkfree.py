from crawler import *

class androidsapkfree_crawler(two_way_crawler):
    def __init__(self):
        super().__init__('http://www.androidapksfree.com/applications/games/',
                         'http://www.androidapksfree.com/applications/apps/',
                         'http://www.androidapksfree.com/applications/games/page/2/',
                         'http://www.androidapksfree.com/applications/apps/page/2/')
        self.folder_name = 'androidapkfree/'
        self.baseUrl = 'http://www.androidapksfree.com'
        if not os.path.exists(self.folder_name):
            os.mkdir(self.folder_name)


    def extraction_routine(self, string):
        apps = re.findall(r'.*href="(http://www.androidapksfree.com/apk/.*?/)".*', string)

        for app in apps:
            try:
                apk_name = app.split('apk/')[1].strip('/') + '.apk'
                if os.path.exists(self.folder_name + apk_name):
                    continue
                else:
                    website = requests.get(app, timeout=self.timeout).text
                    dl_link = re.findall(r'href="(http://.*?\.apk"*?)".*', website)[0]

                    apk_bytes = requests.get(dl_link, allow_redirects=True, stream=True, timeout=self.timeout)

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
        return url.split('page')[0] + 'page/{}/'.format(counter)
