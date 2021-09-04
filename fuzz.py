from DiscoverStrategy import *
from TestStrategy import *
from urllib.parse import urlparse
from options import *
from custom_auth import *
import mechanicalsoup
import sys

browser = mechanicalsoup.StatefulBrowser()


def main():
    (options, args) = parser.parse_args()
    command = sys.argv[1]
    url = sys.argv[2]

    if command == "discover" or command == "test":
        if (options.auth is not None):
            browser = logInDVWA(url, custom_auth)
        else:
            browser = mechanicalsoup.StatefulBrowser()
            browser.open(url)

        if browser.get_current_page() is None:
            parser.error("Cannot reach page.")
        else:
            print("\nVisiting " + url)
            discover(browser, options.words, url, custom_auth)
            
            browser.close

        if command == "test":
            return

        browser.close()
    else:
        parser.error("Invalid command")


if __name__ == "__main__":
    main()
