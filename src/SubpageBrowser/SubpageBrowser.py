class SubpageBrowser:
    def __init__(self):
        pass

    def get_n_subpages(self, number, webpage):
        """
        Function returns list of URLs obtained from given webpage.
        To be used recursively
        :param number: specifies how deep into the search tree should the function proceed
        :param webpage: URL to examine
        :return: list of URLs
        """
        raise NotImplementedError


if __name__ == "__main__":
    Test = 1
    pass
