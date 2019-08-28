import html.parser
import http
import urllib.request
import urllib.parse
import shutil
import pathlib
import sys

def _getHTML(url):
    with urllib.request.urlopen(url) as response:
        if response.getcode() != http.HTTPStatus.OK:
            raise Exception("Failed to get content from " + url + " because " + response.msg)
        return response.read().decode('utf-8')

class _ParseDownloadLinks(html.parser.HTMLParser):
    def __init__(self, srcURL):
        html.parser.HTMLParser.__init__(self)
        self.urllist = []
        self.srcURL = srcURL
    def handle_starttag(self, tag, attrs):
        if tag != 'a':
            return
        for i in attrs:
            if i[0] == 'href':
                url = i[1]
                if sys.platform == 'win32':
                    if not url.endswith('.zip'):
                        continue
                elif not url.endswith(('.tar.gz', 'tar.bz2', 'tar.xz')):
                    continue
                self.urllist.append(urllib.parse.urljoin(self.srcURL, url))

def getDownloadList(url):
    content = _getHTML(url)
    #print(content)

    parser = _ParseDownloadLinks(url)
    parser.feed(content)
    #print(parser.urllist)
    return parser.urllist

def writeDownloadList(url, path):
    dl = getDownloadList(url)
    pathlib.Path(path).write_text("\n".join(dl))

def getDownloadDestPath(url, destDir):
    url_tuple = urllib.parse.urlparse(url)
    filename = pathlib.Path(url_tuple.path).name
    return destDir / filename

def download(url, path):
    if path.exists() and path.is_file():
        print("Skip downloading " + path.name)
        return path
    elif path.is_dir():
        raise IsADirectoryError

    print('downloading ', url)
    with urllib.request.urlopen(url) as response:
        with open(str(path), 'wb') as outfile:
            shutil.copyfileobj(response, outfile)
    return path

