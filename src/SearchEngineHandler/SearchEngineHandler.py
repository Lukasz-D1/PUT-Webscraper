from googlesearch import search
from pprint import pprint


class SearchEngineHandler:
    def __init__(self):
        pass

    def get_results_from_google(self, phrase, how_many_rows):
        """
        Function returns given amount of top Google results
        :param phrase: keyword to be searched
        :param how_many_rows: amount of webpages to get
        :return: list of top n Google results
        """

        google_results = []
        for webpage in search(phrase, tld="com", num=how_many_rows, start=0, stop=how_many_rows, pause=2):
            google_results.append(webpage)
        return google_results

if __name__ == "__main__":
    handler = SearchEngineHandler()
    tab = handler.get_results_from_google('ziemniaczki', 20)
    pprint(tab)
