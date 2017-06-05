# Written by Shivam Sharma KNIT Sultanpur.

# DFS approach in Crawling.
# Google's PageRank algorithm for ranking pages

import re
import urllib
import urllib.request


def generate_in_links(graph):
    in_link = {}
    for key in graph:
        out_list = graph[key]
        for page in out_list:
            if page not in in_link:
                in_link[page] = [key]
            else:
                in_link[page].append(key)
    for key in graph:
        if key not in in_link:
            in_link[key] = []
    return in_link


def compute_ranks(graph):
    d = 0.8  # damping factor
    numloops = 10
    in_link = generate_in_links(graph)
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages

    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            const_factor = (1 - d) / npages
            sum_factor = 0.0
            for incoming in in_link[page]:
                sum_factor = sum_factor + (ranks[incoming] / len(graph[incoming]))
            sum = sum_factor * d
            newranks[page] = const_factor + sum
        ranks = newranks
    return ranks


def union_of(list1, list2):
    for each in list2:
        if each not in list1:
            list1.append(each)
    return list1


def get_page(url):
    # Experimental
    try:
        return str(urllib.request.urlopen(url).read())
    except:
        print('Empty String')
        return ''


def get_links(seed):
    content = get_page(seed)
    links = re.findall(r'http[\w.:&=+_/\-?]+', content)
    return links


# Data structure used for index is a Dictionary.

def add_to_index(index, keyword, url):
    # This procedure is just to add a keyword, url
    # pair to an index. Keywords will be generated in
    # a separate procedure.
    # Using a dictionary. Optimized.
    if keyword in index:
        if url not in index[keyword]:
            index[keyword].append(url)
    else:
        index[keyword] = [url]
    return


def look_up(index, keyword, ranks):
    # Procedure to look-up the keyword in the
    # index given as argument.
    if keyword in index:
        result, sorted_result = index[keyword], []
        for each in result:
            sorted_result.append((each, ranks[each]))
        sorted_result = sorted(sorted_result, key=lambda x: x[1], reverse=True)
        return sorted_result
    return None


def add_page_to_index(index, page_content, url):
    # Procedure that takes up the content of a page
    # along with the url and forms the keywords from the
    # the content. Then adding the keyword into the index.
    words = re.findall(r'[\w]+', page_content)
    for word in words:
        add_to_index(index, word, url)


def crawl(seed):
    # This is the Crawler. Will start off with the seed page. Follow up the
    # links found on that page to reach a point where there are no more pages
    # to crawl to.
    # Returns the index.
    to_be_crawled = [seed]
    crawled = []
    index, graph = {}, {}
    pages_to_crawl = (
        'http://apiboost.000webhostapp.com/',
        'http://shivamsharmas007.000webhostapp.com/',
        'http://shivamsharmas007.000webhostapp.com/tryuserinfo.html',
        'http://shivamsharmas007.000webhostapp.com/trycontestinfo.html',
        'http://shivamsharmas007.000webhostapp.com/tryblog.html',
        'http://shivamsharmas007.000webhostapp.com/tryproblem.html',
        'http://shivamsharmas007.000webhostapp.com/tryavcontests.html'
    )
    while to_be_crawled:
        current_page = to_be_crawled.pop()
        if current_page not in pages_to_crawl:
            continue
        if current_page not in crawled:
            contents = get_page(current_page)  # Storing the contents of the page
            # Invoking the procedure to add the contents into the index
            add_page_to_index(index, contents, current_page)
            out_links = get_links(current_page)
            graph[current_page] = out_links
            if out_links:
                to_be_crawled = union_of(to_be_crawled, out_links)
            crawled.append(current_page)
    return index, graph


# Following call will invoke the crawler with seed page as initial.
print('Welcome to oneSearch!', 'We will be ready in a moment.', sep='\n')
index, graph = crawl('http://apiboost.000webhostapp.com/')
page_rank = compute_ranks(graph)
print('There we Go!')
while True:
    print('Search for ', end=' ')
    query = input()
    relevant_pages = look_up(index, query, page_rank)
    print('Your Search : ')
    if relevant_pages:
        for each in relevant_pages:
            print(each[0])
    else:
        print('No such result.')
    print('Want to search more? ', end=' ')
    choice = input()
    if choice == 'no' or choice == 'NO' or choice == 'No':
        print('Thank you for choosing us.')
        break
