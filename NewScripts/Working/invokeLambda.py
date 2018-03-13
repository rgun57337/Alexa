def protalStatus(urls):
    import httplib
    from urlparse import urlparse

    def checkUrl(url):
        p = urlparse(url)
        conn = httplib.HTTPConnection(p.netloc)
        conn.request('HEAD', p.path)
        resp = conn.getresponse()
        return resp.status

    workingURLS = []
    nonWorkingURLs = []
    responseURLs = ""
    for url in urls:
        if checkUrl(url) == 200:
            workingURLS.append(url)
        else:
            nonWorkingURLs.append(url)

    if len(nonWorkingURLs) > 0:
        responseURLs += str(len(nonWorkingURLs)) + " URLs are down and running. They are. \n"
        for nonWorkingURL in nonWorkingURLs:
            responseURLs += nonWorkingURL + ".\n"
    else:
        responseURLs = "All the URLs up and running."

    return responseURLs

URLs = ['http://www.stackoverflow.com','http://stackoverflow.com/notarealpage.html','https://www.google.com','http://youtube.com']
print(protalStatus(URLs))
