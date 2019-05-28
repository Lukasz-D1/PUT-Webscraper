import tkinter
import tkinter.messagebox as msgBox
from src.WebpageAnalyzer.WebpageAnalyzer import WebpageAnalyzer
from src.SearchEngineHandler.SearchEngineHandler import SearchEngineHandler


class WebscrapperGUI:
    def __init__(self):
        self.anal = WebpageAnalyzer()
        self.search_engine_handler = SearchEngineHandler()
        pass

    def start(self):
        # Main window
        WindowMain = tkinter.Tk("Webscraper")
        WindowMain.geometry("650x300")
        WindowMain.resizable(1, 1)
        WindowMain.title("Webscraper")

        # Variables used in the GUI
        stringGoogle = tkinter.StringVar()
        stringGoogleN = tkinter.StringVar()
        stringGoogleLabel = tkinter.StringVar()
        stringGoogle.set("ziemniaczki")
        stringGoogleN.set("5")
        stringGoogleLabel.set("Phrase\t")

        self.stringURL = tkinter.StringVar()
        stringURLLabel = tkinter.StringVar()
        stringURLLabel.set("URLs to scrap:\t")
        self.stringURL.set("http://fee.put.poznan.pl http://pyszne.pl http://wykop.pl")

        stringFilename = tkinter.StringVar()
        stringFilenameLabel = tkinter.StringVar()
        stringFilenameLabel.set("Output filename:\t")
        stringFilename.set("output.txt")

        stringSubpagesLabel = tkinter.StringVar()
        stringSubpagesLabel.set("Subpages to scrap:\t")
        stringSubpagesNumber = tkinter.StringVar()
        stringSubpagesNumber.set("2")

        stringThresholdLabel = tkinter.StringVar()
        stringMinThresh = tkinter.StringVar()
        stringMaxThresh = tkinter.StringVar()
        stringThresholdLabel.set("Image threshold in bytes:")
        stringMinThresh.set("10")
        stringMaxThresh.set("10000000")

        # The GUI elements
        frame_google = tkinter.Frame(WindowMain, height=20)
        frame_google.pack_propagate(0)
        LabelGoogle = tkinter.Label(frame_google, textvariable=stringGoogleLabel)
        EntryGoogle = tkinter.Entry(frame_google, width=30, textvariable=stringGoogle)
        EntryGoogleN = tkinter.Entry(frame_google, width=10, textvariable=stringGoogleN)
        ButtonGoogle = tkinter.Button(frame_google, text="Get Google results",
                                      command=lambda: self.update_textbox_with_google_results(stringGoogle.get(),
                                                                                              int(stringGoogleN.get())))
        frame_url_input = tkinter.Frame(WindowMain, height=20)
        frame_url_input.pack_propagate(0)
        LabelURLInput = tkinter.Label(frame_url_input, textvariable=stringURLLabel)
        EntryURLInput = tkinter.Entry(frame_url_input, width=60, textvariable=self.stringURL)

        frame_links = tkinter.Frame(WindowMain, height=20)
        frame_links.pack_propagate(0)
        LabelFilenameInput = tkinter.Label(frame_links, textvariable=stringFilenameLabel)
        EntryFilenameInput = tkinter.Entry(frame_links, width=40, textvariable=stringFilename)
        ButtonGetLinks = tkinter.Button(frame_links, text="Get links",
                                        command=lambda: self.get_links_from_textbox(self.stringURL.get(),
                                                                                    stringFilename.get()))

        frame_subpages = tkinter.Frame(WindowMain, height=20)
        frame_subpages.pack_propagate(0)
        EntrySubpagesNumber = tkinter.Entry(frame_subpages, width=5, textvariable=stringSubpagesNumber)
        LabelSubpages = tkinter.Label(frame_subpages, textvariable=stringSubpagesLabel)
        ButtonGetSubpages = tkinter.Button(frame_subpages, text="Scrap subpages",
                                           command=lambda: self.get_subpages_from_textbox(self.stringURL.get(),
                                                                                          stringFilename.get(), int(
                                                   stringSubpagesNumber.get())))

        frame_images = tkinter.Frame(WindowMain, height=20)
        frame_images.pack_propagate(0)
        EntryMinThresh = tkinter.Entry(frame_images, width=15, textvariable=stringMinThresh)
        EntryMaxThresh = tkinter.Entry(frame_images, width=15, textvariable=stringMaxThresh)
        LabelThreshold = tkinter.Label(frame_images, textvariable=stringThresholdLabel)
        ButtonGetImages = tkinter.Button(frame_images, text="Get images",
                                         command=lambda: self.get_images_from_textbox(self.stringURL.get(), "images/",
                                                                                      int(stringMinThresh.get()),
                                                                                      int(stringMaxThresh.get())))

        frame_google.pack(fill=tkinter.X, expand=False, padx=15, pady=15)
        LabelGoogle.pack(side=tkinter.LEFT)
        EntryGoogle.pack(side=tkinter.LEFT)
        EntryGoogleN.pack(side=tkinter.LEFT)
        ButtonGoogle.pack(side=tkinter.RIGHT, padx=15)

        frame_url_input.pack(fill=tkinter.X, expand=False, padx=15, pady=15)
        LabelURLInput.pack(side=tkinter.LEFT)
        EntryURLInput.pack(side=tkinter.LEFT)

        frame_links.pack(fill=tkinter.X, expand=False, padx=15, pady=15)
        LabelFilenameInput.pack(side=tkinter.LEFT)
        EntryFilenameInput.pack(side=tkinter.LEFT)
        ButtonGetLinks.pack(side=tkinter.RIGHT, padx=15)

        frame_subpages.pack(fill=tkinter.X, expand=False, padx=15, pady=15)
        LabelSubpages.pack(side=tkinter.LEFT)
        EntrySubpagesNumber.pack(side=tkinter.LEFT)
        ButtonGetSubpages.pack(side=tkinter.RIGHT, padx=15)

        frame_images.pack(fill=tkinter.X, expand=False, padx=15, pady=15)
        LabelThreshold.pack(side=tkinter.LEFT)
        EntryMinThresh.pack(side=tkinter.LEFT)
        EntryMaxThresh.pack(side=tkinter.LEFT)
        ButtonGetImages.pack(side=tkinter.RIGHT, padx=15)

        WindowMain.mainloop()

    def update_textbox_with_google_results(self, phrase, rows):
        urls = self.search_engine_handler.get_results_from_google(phrase, how_many_rows=rows)
        string = ""
        for url in urls:
            string += url + " "
        self.stringURL.set(string[:-1])

    def get_links_from_textbox(self, urls, filename):
        try:
            # links = self.anal.get_urls_with_description(url, filename)
            url_list = urls.split(" ")
            links, length = self.anal.scrap_multiple_websites(url_list, filename)
            msgBox.showinfo("Done", f"Saved {length} links to {filename}.")
        except Exception as e:
            msgBox.showerror("Error", f"Couldn't scrap the URL:\n {e}")

    def get_images_from_textbox(self, urls, location, min_threshold, max_threshold):
        try:
            url_list = urls.split(" ")

            count = self.anal.scrap_multiple_images(url_list, location, min_threshold, max_threshold)

            msgBox.showinfo("Done", f"Downloaded {count} images to {location}.")

        except Exception as e:
            msgBox.showerror("Error", f"Couldn't scrap the URL:\n {e}")

    def get_subpages_from_textbox(self, urls, filename, depth):
        try:
            url_list = urls.split(" ")
            count = 0
            for url in url_list:
                count += len(self.anal.scrap_subpages(depth, url, filename))

            msgBox.showinfo("Done", f"Saved {count} links to {filename}.")

        except Exception as e:
            msgBox.showerror("Error", f"Couldn't scrap the URL:\n {e}")


if __name__ == "__main__":
    g = WebscrapperGUI()
    g.start()
