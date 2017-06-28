from crawler import *

class fdroid_crawler(crawler):
    def __init__(self):
        super().__init__('https://f-droid.org/repository/browse/',
                         'https://f-droid.org/repository/browse/?fdpage=2')
        self.folder_name = 'fdroid/'
        if not os.path.exists(self.folder_name):
            os.mkdir(self.folder_name)

    def mutate_url(self, url, counter):
        result = 'https://f-droid.org/repository/browse/?fdpage={}'.format(counter+1)
        return result

    def extraction_routine(self, string):
        apps = re.findall(r'.*href="(https://f-droid.org/repository/browse/\?fdid=.*?)".*', string)
        apps.extend(re.findall(r'.*href="(https://f-droid.org/repository/browse/\?fdid=.*?&fdpage=.*?)".*', string))

        for app in apps:
            try:
                website = requests.get(app, timeout=self.timeout).text
                dl_links = re.findall(r'href="(https://f-droid.org/repo/.*?\.apk)"', website)
                for link in dl_links:
                    try:
                        apk_name = link.split('/')[-1]
                        if os.path.exists(self.folder_name + apk_name):
                            continue
                        else:
                            apk_bytes = requests.get(link, allow_redirects=True, stream=True, timeout=self.timeout)

                            with open(self.folder_name + apk_name, 'wb') as f:
                                for chunk in apk_bytes.iter_content(chunk_size=1024):
                                    if chunk:  # filter out keep-alive new chunks
                                        f.write(chunk)
                    except:
                        pass
            except:
                pass
