import mechanicalsoup


def test(browser, url):
    browser.open(url)
    print("Visiting " + browser.get_url() + "\n")
