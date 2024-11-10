import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    
    # print("1.html: ")
    # transition_model(corpus, '1.html', DAMPING)
    # print("2.html: ")
    # transition_model(corpus, '2.html', DAMPING)
    # print("3.html: ")
    # transition_model(corpus, '3.html', DAMPING)
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # get the probability of randomly choosing any page (1 - damping_factor)
    probability_any = (1 - damping_factor) / len(corpus)

    probability_distribution = {key: probability_any for key in corpus}
    
    # if page has no outgoing links, return probability distribution that chooses randomly among all pages
    if page not in corpus:
        raise ValueError(f"Page '{page}' not found in corpus")
    if not corpus[page]:
        for key in probability_distribution:
            probability_distribution[key] += damping_factor/len(corpus)
        return probability_distribution
    
    # With probability damping_factor, the random surfer should randomly choose
    # one of the links from page with equal probability.
    probability = damping_factor / len(corpus[page])
    for key in probability_distribution:
        if key in corpus[page]:
            probability_distribution[key] += probability
    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = list(corpus.keys())
    starting_page = random.choice(pages)
    pagerank = transition_model(corpus, starting_page, damping_factor)
    pageRanks = dict()
    i = 0
    while i < n:
        selected_page = random.choices(pages, weights=pagerank.values())[0]
        if selected_page in pageRanks:
            pageRanks[selected_page] += 1
        else:
            pageRanks[selected_page] = 1

        pagerank = transition_model(corpus, selected_page, damping_factor)

        i += 1
    for key in pageRanks:
        pageRanks[key] = pageRanks[key] / n
    return pageRanks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    n = len(corpus)
    pageRanks = {key: 1 / n for key in corpus}
    new_PageRanks = pageRanks.copy()
    max_difference = 0.001

    while True:
        for page in corpus:
            pr = (1 - damping_factor) / n
            for p in corpus:
                if page in corpus[p]: # if there is a page with a link to the page we are currently on
                    pr += damping_factor * pageRanks[p] / len(corpus[p])
            new_PageRanks[page] = pr

        exact_enough = False
        for page in pageRanks:
            if abs(pageRanks[page] - new_PageRanks[page]) <= max_difference:
                exact_enough = True
            else:
                exact_enough = False
        if exact_enough:
            break
        pageRanks = new_PageRanks.copy()
    
    return pageRanks


if __name__ == "__main__":
    main()
