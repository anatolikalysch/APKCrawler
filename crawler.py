import requests
import re
import os

class crawler(object):
    def __init__(self, url, templateUrl):
        self.baseUrl = url
        self.template = templateUrl
        self.counter = 1
        self.timeout = 10

    def start_crawl(self):
        startpage = requests.get(self.baseUrl, timeout=self.timeout).text

        try:
            self.extraction_routine(startpage)
        except:
            pass

        while True:
            try:
                self.extraction_routine(requests.get(self.mutate_url(self.template, self.counter), timeout=self.timeout).text)
                self.counter += 1
            except Exception as e:
                print(e.args)
                self.counter += 1

    def extraction_routine(self, string):
        pass

    def mutate_url(self, url, counter):
        pass

class two_way_crawler(object):
    def __init__(self, gameUrl, softUrl, templGame, templSoft):
        self.baseGameUrl = gameUrl
        self.baseSoftUrl = softUrl
        self.templateSoft = templSoft
        self.templateGame = templGame
        self.counter = 2
        self.timeout = 10
        self.game = False

    def start_crawl(self):
        try:
            self.game = True
            startpage = requests.get(self.baseGameUrl, timeout=self.timeout).text
            self.extraction_routine(startpage)
            self.game = False
            startpage = requests.get(self.baseSoftUrl, timeout=self.timeout).text
            self.extraction_routine(startpage)
        except Exception as e:
                print(e.args)

        while True:
            try:
                self.game = True
                self.extraction_routine(requests.get(self.mutate_url(self.templateGame, self.counter), timeout=self.timeout).text)
                self.game = False
                self.extraction_routine(requests.get(self.mutate_url(self.templateSoft, self.counter), timeout=self.timeout).text)
                self.counter += 1
            except Exception as e:
                print(e.args)
                self.counter += 1

    def extraction_routine(self, string):
        pass

    def mutate_url(self, url, counter):
        pass
