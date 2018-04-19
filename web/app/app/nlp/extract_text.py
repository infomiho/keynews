import requests
import re
from readability import Document
from bs4 import BeautifulSoup


def get_article(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=4) # can throw BaseException if the server does not respond, or TooManyRedirects
    except BaseException:
        return ''

    readability_doc = Document(response.text)

    # doc.summary() is not really a summary just the main part of the
    # website's content
    html_content = readability_doc.summary()
    title = readability_doc.title()
    soup = BeautifulSoup(html_content, 'html.parser')
    # Replace all excesive whitespace and new line
    content = re.sub(r"(\s{2,})|(\n{2,})", "\n",
                     soup.get_text(), flags=re.UNICODE)
    if " - " in title:
        title = re.sub(
            r" - [\s\w]+$",
            "",
            title
        )

    return content, title
