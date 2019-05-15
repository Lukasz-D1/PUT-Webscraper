import requests
import bs4
import urllib.request
from pprint import pprint
import time
from urllib.parse import urlparse
import os
import json

class WebpageAnalyzer:
    def __init__(self):
        self.many_urls = []


    def get_webpage_source(self, webpage_url):
        """
        Returns source of given webpage or raises exception if page not accessible
        :param webpage_url: URL to obtain source code from
        :return: string of raw source code, webpage url from response
        """
        response = requests.get(webpage_url)
        if response.status_code == 200:
            u = urlparse(response.url)
            link = u.scheme + "://" + u.netloc
            return response.text, link
        else:
            raise Exception(f"Source not obtained, response status code: [{response.status_code}]")

    def get_images(self, webpage_url, location, min_threshold=0, max_threshold=10000000):
        """
        Analyzes given webpage and downloads all images meeting given requirements
        :param webpage_url: URL to the site to download images from
        :param location: location to which images will be saved
        :param min_threshold: minumum image size in bytes
        :param max_threshold: maximum image size in bytes
        :return: number of images downloaded
        """
        webpage_source, webpage_url_from_request = self.get_webpage_source(webpage_url)

        soup = bs4.BeautifulSoup(webpage_source, features="html.parser")

        images = []
        for img in soup.findAll('img'):
            image = img.get('src')
            if image is None:
                image = img.get('data-original')
            if image is not None:
                images.append(image)

        images_for_download = []
        for i in images:
            if i[:4] != "http":
                file_name = webpage_url + i
                file = urllib.request.urlopen(file_name)
                file_size = len(file.read())
                if file_size > min_threshold and file_size<max_threshold:
                    images_for_download.append(file_name)
            else:
                file_name = i
                file = urllib.request.urlopen(file_name)
                file_size = len(file.read())
                if file_size > min_threshold and file_size < max_threshold:
                    images_for_download.append(file_name)

        if not os.path.exists(location):
            os.makedirs(location)

        for i in images_for_download:
            name = i.split('/')[-1]
            if name.__contains__('?'):
                name=name.replace('?','')
            # if name.endswith('.png')!= 1 and name.endswith('.jpg')!=1:
            #     name=name+'.png'
            urllib.request.urlretrieve(i, location + str(time.time()) + "_" + name)

        return len(images)

    def get_urls_with_description(self, webpage_url, file_location=None):
        """
        Analyzes given webpage and returns list of tuples with links and descriptions found,
        optionally saves obtained data to the file
        :param webpage_url: URL to the webpage to process
        :param file_location: optional location to which file with, None can be passed
        :return: list of tuples {url : description of link}
        """

        webpage_source, webpage_url_from_request = self.get_webpage_source(webpage_url)

        soup = bs4.BeautifulSoup(webpage_source, features="html.parser")

        output_tuple_list = []
        for a in soup.find_all('a', href=True):
            if a['href'][:4] != "http":
                # if url does not start with a word "http" add webpage address to the beginning
                result_tuple = (webpage_url_from_request + a['href'], a.string)
            else:
                result_tuple = (a['href'], a.string)
            output_tuple_list.append(result_tuple)

        if file_location:
            # save results in the file
            file = open(file_location, 'a+')
            for item in output_tuple_list:
                file.write(item[0] + "\t" + str(item[1]) + "\n")

        return output_tuple_list

    def scrap_multiple_websites(self, websites_list, file_location=None):
        """
        Analyzes given webpages and returns list of tuples with links and descriptions found,
        optionally saves obtained data to the file
        :param websites_list: list of webpages to scrap
        :param file_location: optional location to which file with, None can be passed
        :return: List of tuples {url : description of link}
        """
        output_tuple_list = []
        for site in websites_list:
            print("Scraping:", site)
            urls = self.get_urls_with_description(site, file_location)
            output_tuple_list += urls
        return output_tuple_list

    def scrap_subpages_filip(self, depth, website):
        output = dict()
        output[website] = 0
        for _ in range(depth):
            for key, value in output.copy().items():
                if value == 0:
                    try:
                        subpages = self.get_urls_with_description(key)
                        for subpage in subpages:
                            if subpage[0] not in output.keys():
                                output[subpage[0]] = 0
                                print(".", end='')
                    except:
                        print("smth")
                output[key] = value + 1
        from pprint import pprint
        pprint(output)
        return output

    def scrap_subpage(self, depth, website):
        self.many_urls.append(website)
        results = self.get_urls_with_description(website)

        for result in results:
            wyniki = self.get_urls_with_description(website)
            print(wyniki)
            next = result[0]
            if next not in self.many_urls:
                self.many_urls.append(next)
                break
            else:
                continue

        print(str(depth) + " at " +website)
        print(results)
        if depth == 1:
            return 1
        return self.scrap_subpage(depth-1, next)


    def scrap_subpage_iter(self, depth, website):
        visited_urls = []
        results = self.get_urls_with_description(website)
        visited_urls.append(website)
        # for result in results:
        #     for i in range(depth):
        #         iter = 0
        #         while iter < 10:
        #             deep_results = self.get_urls_with_description(result[0])
        #             for deep_result in deep_results:
        #                 if deep_result[0] in visited_urls:
        #                     continue
        #                 else:
        #                     visited_urls.append(deep_result[0])
        #                     print(deep_result[0]+"\n")
        #                     print(deep_results)
        #                     iter += 1
        iter = 0
        i = 0
        deep = 1

        while iter < 2:
            temp = results[i][0]
            iterA = 0
            iA = 0
            if results[i][0] not in visited_urls and website in results[i][0]:
                deep_results = self.get_urls_with_description(results[i][0])
                visited_urls.append(results[i][0])
                print("\n" + str(deep)+ results[i][0])
                print(deep_results)

                while iterA < 2:
                    deep +=1
                    tempA = deep_results[iA][0]
                    if deep_results[iA][0] not in visited_urls and website in deep_results[iA][0]:
                        deeper_results = self.get_urls_with_description(deep_results[iA][0])
                        print("\n" + str(deep) + deep_results[iA][0])
                        print(deeper_results)


                        iterA+=1
                        visited_urls.append(deep_results[iA][0])
                    iA+=1
                    deep -= 1

                iter+=1
            i+=1

if __name__ == "__main__":
    anal = WebpageAnalyzer()

    websites_list = ["http://www.pyszne.pl", "http://fee.put.poznan.pl/index.php/en/"]

    images = anal.get_images("http://wykop.pl", "images/",0,1000000)
    urls = anal.scrap_multiple_websites(websites_list, "file.txt")

    pprint(urls)
    #sanal.scrap_subpage(depth=6, website="https://www.michalwolski.pl")
    anal.scrap_subpage_iter(depth=6, website="https://www.michalwolski.pl")

   # anal.scrap_subpages(2, "http://www.michalwolski.pl/")
    anal.get_urls_with_description("http://www.pyszne.pl")
