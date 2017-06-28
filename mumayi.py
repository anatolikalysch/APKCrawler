from crawler import *

class mumayi_crawler(crawler):
    def __init__(self):
        super().__init__('http://down.mumayi.com/', 'http://down.mumayi.com/1')
        self.folder_name = 'mumayi/'
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
        apk_name = str(ctr) + '.apk'
        try:
            if os.path.exists(self.folder_name + apk_name):
                pass
            else:
                self.download(apk_name, ctr)
        except requests.exceptions.Timeout:
            try:
                self.download(apk_name, ctr)
            except Exception as e:
                print(e.args)
        except Exception as e:
            print(e.args)

    def download(self, apk_name, ctr):
        apk_bytes = requests.get('http://down.mumayi.com/{}'.format(ctr), allow_redirects=True, stream=True,
                                 timeout=self.timeout)
        if apk_bytes.status_code != 200:
            pass
        else:
            with open(self.folder_name + apk_name, 'wb') as f:
                for chunk in apk_bytes.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)