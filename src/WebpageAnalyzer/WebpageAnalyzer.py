class WebpageAnalyzer:
    def __init__(self):
        pass

    def get_images(self, webpage, location, min_threshold, max_threshold):
        """
        Analyzes given webpage and downloads all images meeting given requirements
        :param webpage: URL to the site to download images from
        :param location: location to which images will be saved
        :param min_threshold: minumum image size in bytes
        :param max_threshold: maximum image size in bytes
        :return: number of images downloaded
        """

        raise NotImplementedError

    def get_urls_with_description(self, webpage, location=None):
        """
        Analyzes given webpage and returns list of tuples with links and descriptions found,
        optionally saves obtained data to the file
        :param webpage: URL to the webpage to process
        :param location: optional location to which file with, None can be passed
        :return: list of tuples {url : description of link}
        """

        raise NotImplementedError


if __name__ == "__main__":
    pass
