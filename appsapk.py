from crawler import *


class appsapk_crawler(crawler):
    def __init__(self):
        super().__init__('http://www.appsapk.com/android/all-apps/',
                         'http://www.appsapk.com/android/all-apps/page/2/')
        self.urlBase = 'http://www.appsapk.com'
        self.folder_name = 'appsapk/'
        if not os.path.exists(self.folder_name):
            os.mkdir(self.folder_name)

    def mutate_url(self, url, counter):
        result = 'https://www.appsapk.com/android/all-apps/page/{}/'.format(self.counter)
        return result

    def extraction_routine(self, string):
        apps = re.findall(r'.*href="(http://www.appsapk.com/.*?/)".*', string)
        apps.extend(re.findall(r'.*href="(https://www.appsapk.com/.*?/)".*', string))
        for app in apps:
            try:
                app_website = requests.get(app, timeout=self.timeout, headers=self.header).text
                dl_link = re.findall('.*href="(http://.*?appsapk\.com/.*?\.apk)".*', app_website)[0]
                apk_name = dl_link.split('/')[-1]
                if os.path.exists(self.folder_name + apk_name):
                    continue
                else:
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
