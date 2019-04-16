import requests
import bs4

class WebpageAnalyzer:
    def __init__(self):
        pass

    def get_webpage_source(self, webpage_url):
        """
        Returns source of given webpage or raises exception if page not accessible
        :param webpage_url: URL to obtain source code from
        :return: string of raw source code
        """
        response = requests.get(webpage_url)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Source not obtained, response status code: [{response.status_code}]")

    def get_images(self, webpage_source, location, min_threshold, max_threshold):
        """
        Analyzes given webpage and downloads all images meeting given requirements
        :param webpage: URL to the site to download images from
        :param location: location to which images will be saved
        :param min_threshold: minumum image size in bytes
        :param max_threshold: maximum image size in bytes
        :return: number of images downloaded
        """

        raise NotImplementedError

    def get_urls_with_description(self, webpage_url, location=None):
        """
        Analyzes given webpage and returns list of tuples with links and descriptions found,
        optionally saves obtained data to the file
        :param webpage_url: URL to the webpage to process
        :param location: optional location to which file with, None can be passed
        :return: list of tuples {url : description of link}
        """

        try:
            webpage_source = self.get_webpage_source(webpage_url)
        except Exception:
            raise Exception("URLs not obtained")

        soup = bs4.BeautifulSoup(webpage_source, features="html.parser")

        output_tuple_list = []
        for a in soup.find_all('a', href=True):
            if a['href'][:4] != "http":
                result_tuple = (webpage_url + a['href'], a.string)
            else:
                result_tuple = (a['href'], a.string)
            output_tuple_list.append(result_tuple)

        return output_tuple_list

    websites_list = ["http://www.pyszne.pl", "http://fee.put.poznan.pl/index.php/en/"]

    def scrap_multiple_websites(self, websites_list):
        for site in websites_list:
            print(site)
            self.get_urls_with_description(site)


if __name__ == "__main__":
    anal = WebpageAnalyzer()
    anal.get_urls_with_description("http://www.pyszne.pl")
