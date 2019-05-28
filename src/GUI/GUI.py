import tkinter
import tkinter.messagebox as msgBox
from src.WebpageAnalyzer.WebpageAnalyzer import WebpageAnalyzer


class WebscrapperGUI:
    def __init__(self):
        self.anal = WebpageAnalyzer()
        pass

    def start(self):
        # Main window
        WindowMain = tkinter.Tk("Webscrapper")
        WindowMain.geometry("600x300")
        WindowMain.resizable(0, 0)
        WindowMain.title("Webscrapper")

        # Variables used in the GUI
        stringURL = tkinter.StringVar()
        stringURLLabel = tkinter.StringVar()

        stringFilename = tkinter.StringVar()
        stringFilenameLabel = tkinter.StringVar()

        stringURLLabel.set("URL:\t\t")
        stringFilenameLabel.set("Output filename:\t")

        stringURL.set("http://fee.put.poznan.pl http://pyszne.pl http://wykop.pl")
        stringFilename.set("output.txt")

        # The GUI elements
        FrameInputURL = tkinter.Frame(WindowMain)
        FrameInputURL.pack_propagate(0)
        FrameInputFilename = tkinter.Frame(WindowMain)
        FrameInputFilename.pack_propagate(0)
        FrameButtons = tkinter.Frame(WindowMain)
        FrameButtons.pack_propagate(0)

        LabelURLInput = tkinter.Label(FrameInputURL, textvariable=stringURLLabel)
        EntryURLInput = tkinter.Entry(FrameInputURL, width=100, textvariable=stringURL)
        LabelFilenameInput = tkinter.Label(FrameInputFilename, textvariable=stringFilenameLabel)
        EntryFilenameInput = tkinter.Entry(FrameInputFilename, width=100, textvariable=stringFilename)

        ButtonGetLinks = tkinter.Button(FrameButtons, text="Get links",
                                        command=lambda: self.get_links_from_textbox(stringURL.get(),
                                                                                    stringFilename.get()))
        ButtonGetImages = tkinter.Button(FrameButtons, text="Get images",
                                         command=lambda: self.get_images_from_textbox(stringURL.get(), "images/", 10, 100000))

        # Packing the elements
        FrameInputURL.pack(fill=tkinter.BOTH, expand=True)
        LabelURLInput.pack(side=tkinter.LEFT)
        EntryURLInput.pack(side=tkinter.RIGHT)

        FrameInputFilename.pack(fill=tkinter.BOTH, expand=True)
        LabelFilenameInput.pack(side=tkinter.LEFT)
        EntryFilenameInput.pack(side=tkinter.RIGHT)

        FrameButtons.pack(fill=tkinter.BOTH, expand=True)
        ButtonGetImages.pack(side=tkinter.TOP)
        ButtonGetLinks.pack(side=tkinter.TOP)

        # Setting everything in motion
        WindowMain.mainloop()

    def get_links_from_textbox(self, urls, filename):
        try:
            # links = self.anal.get_urls_with_description(url, filename)
            url_list = urls.split(" ")
            links = self.anal.scrap_multiple_websites(url_list, filename)
            msgBox.showinfo("Done", f"Saved {len(links)} links to {filename}.")
        except Exception as e:
            msgBox.showerror("Error", f"Couldn't scrap the URL:\n {e}")

    def get_images_from_textbox(self, urls, location, min_threshold, max_threshold):
        try:
            url_list = urls.split(" ")
            count = 0
            for url in url_list:
                count += self.anal.get_images(url, location, min_threshold, max_threshold)

            msgBox.showinfo("Done", f"Downloaded {count} images to {location}.")

        except Exception as e:
            msgBox.showerror("Error", f"Couldn't scrap the URL:\n {e}")


if __name__ == "__main__":
    g = WebscrapperGUI()
    g.start()
