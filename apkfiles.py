from crawler import *

class apkfiles_crawler(crawler):
    def __init__(self):
        super().__init__('https://www.apkfiles.com', 'https://www.apkfiles.com/apk-')
        self.folder_name = 'apkfiles/'
        if not os.path.exists(self.folder_name):
            os.mkdir(self.folder_name)

    def start_crawl(self):
        while True:
            try:
                self.extraction_routine(self.counter)
                self.counter += 1
            except Exception as e:
                break

    def extraction_routine(self, ctr):
        try:
            website = requests.get(self.template + str(ctr), timeout=self.timeout).text
            dl_link = re.findall(r'.*href="(/download/.*?\.apk\?key=.*?)"', website)[0]
            apk_name = dl_link.split('.apk')[0].split('/')[-1] + '.apk'
            if os.path.exists(self.folder_name + apk_name):
                pass
            else:
                apk_bytes = requests.get(self.baseUrl + dl_link, allow_redirects=True, stream=True, timeout=self.timeout)

                with open(self.folder_name + apk_name, 'wb') as f:
                    for chunk in apk_bytes.iter_content(chunk_size=1024):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
        except:
            pass