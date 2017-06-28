from crawler import *


class slideme_crawler(crawler):
    def __init__(self):
        super().__init__('http://slideme.org/applications?filters=tfs_price%3A%5B0%20TO%200%5D&solrsort=created%20asc',
                         'http://slideme.org/applications?page=1&filters=tfs_price%3A%5B0%20TO%200%5D&solrsort=created%20asc')
        self.urlBase = 'http://slideme.org'
        self.folder_name = 'slideme/'
        if not os.path.exists(self.folder_name):
            os.mkdir(self.folder_name)


    def extraction_routine(self, string):
        apps = re.findall(r'.*"(/application/.*?)">.*', string)
        for app in apps:
            try:
                app_website = requests.get(self.urlBase + app, timeout=self.timeout).text
                dl_link = re.findall('<a href="(https://slideme.org/.*?.apk\?adl=.*?)"', app_website)[0]
                apk_name = app.split('/')[2] + '.apk'
                if os.path.exists(self.folder_name + apk_name):
                    continue
                else:
                    apk_bytes = requests.get(dl_link, allow_redirects=True, stream=True, timeout=self.timeout)

                    with open(self.folder_name + apk_name, 'wb') as f:
                        for chunk in apk_bytes.iter_content(chunk_size=1024):
                            if chunk:  # filter out keep-alive new chunks
                                f.write(chunk)
            except Exception as e:
                pass

    def mutate_url(self, url, counter):
        result = re.sub(r'page=.*?&', 'page={}&'.format(counter), url)
        return result
