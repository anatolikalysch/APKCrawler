# Third Party Android App Store Crawlers

These are sample crawlers for several Android app stores. 
All are written in python3 and offer basic functionality.
Their purpose is to crawl stores for .apk files to create a repository of APKs. 
Such a repository could be used for different purposes, e.g. scientific studies or malware analysis.

_This project is **not** actively developed. The use of crawlers might have legal repercussions in your country. The crawlers are provided as is and under no warranty what so ever._


##The following app stores are supported:

 - androidapkfree
 - anruan
 - apkfiles
 - apkmirrordownload
 - apkpure
 - appsapk
 - aptoide
 - eoemarket
 - fdroid
 - hiapk
 - mobileapkworld
 - mumayi
 - nduo
 - 1appmarket
 - play mob
 - baidu
 - slideme
 - up2down
 
 ##Usage:
 ```python
from store_of_your_choice import crawler_of_your_choice() 
c = crawler_of_your_choice()
c.start_crawl()
```
 

