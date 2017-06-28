from crawler import *


class play_mob_crawler(crawler):
    def __init__(self):
        super().__init__('http://play.mob.org/',
                         'http://play.mob.org/page-2/')
        self.urlBase = 'http://play.mob.org/'
        self.folder_name = 'play_mob/'
        if not os.path.exists(self.folder_name):
            os.mkdir(self.folder_name)

    def mutate_url(self, url, counter):
        result = 'http://play.mob.org/page-{}/'.format(self.counter)
        return result

    def extraction_routine(self, string):
        apps = re.findall(r'.*href="(http://play.mob.org/game/.*?.html)".*', string)
        for app in apps:
            try:
                app_website = requests.get(app, timeout=self.timeout, headers=self.header).text
                dl_link = re.findall('.*href="(http://play.mob.org/android/.*?\.apk)".*', app_website)
                for link in dl_link:
                    apk_name = link.split('/')[-1]
                    if os.path.exists(self.folder_name + apk_name):
                        continue
                    else:
                        apk_bytes = requests.get(link, allow_redirects=True, stream=True, timeout=self.timeout,
                                                 headers=self.header)

                        with open(self.folder_name + apk_name, 'wb') as f:
                            for chunk in apk_bytes.iter_content(chunk_size=1024):
                                if chunk:  # filter out keep-alive new chunks
                                    f.write(chunk)

            except Exception as e:
                pass
