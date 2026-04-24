import tldextract

def get_domain(url):
    ext = tldextract.extract(url)
    return ext.domain

def is_same_site(url1, url2):
    return get_domain(url1) == get_domain(url2)