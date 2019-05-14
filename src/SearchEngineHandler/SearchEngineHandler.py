from googlesearch import search

class SearchEngineHandler:
    def __init__(self):
        pass

    def get_n_addresses(self, number, keyword):
        """
        Function returns given amount of top Google results
        :param number: amount of webpages to get
        :param keyword: keyword to be searched
        :return: list of top n Google results
        """

        raise NotImplementedError

    def get_results_from_google(self, phrase, how_many_rows):
        tab = []
        for i in search(phrase, tld="com", num=how_many_rows, start=0, stop=how_many_rows, pause=2):
            tab.append(i)
        return tab


if __name__ == "__main__":
    handler = SearchEngineHandler()
    tab = handler.get_results_from_google('ziemniaczki',20)
    for i in tab:
        print(i)
