from crawler import *

class apkmirrordownload_crawler(crawler):
    def __init__(self):
        super().__init__('https://www.apkmirrordownload.com/',
                         'https://www.apkmirrordownload.com/page/2/')
        self.urlBase = 'http://www.apkmirrordownload.com'
        self.folder_name = 'apkmirrordownload/'
        if not os.path.exists(self.folder_name):
            os.mkdir(self.folder_name)

    def mutate_url(self, url, counter):
        result = 'https://www.apkmirrordownload.com/page/{}/'.format(self.counter)
        return result


    def extraction_routine(self, string):
        apps = re.findall(r'.*href="(https://www.apkmirrordownload.com/apk/.*?)" title=".*', string)
        for app in apps:
            try:
                app_website = requests.get(app, timeout=self.timeout).text
                dl_link = re.findall('.*href="//apkmirrordownload.com(/wp-content/themes/apkmirrordownload/download\.php\?type=apk.*?id=.*?)".*', app_website)[0]
                apk_name = app.split('/apk/')[1].rstrip('/') + '.apk'
                if os.path.exists(self.folder_name + apk_name):
                    continue
                else:
                    apk_bytes = requests.get(self.urlBase + dl_link, allow_redirects=True, stream=True, timeout=self.timeout)

                    with open(self.folder_name + apk_name, 'wb') as f:
                        for chunk in apk_bytes.iter_content(chunk_size=1024):
                            if chunk:  # filter out keep-alive new chunks
                                f.write(chunk)
            except Exception as e:
                pass

