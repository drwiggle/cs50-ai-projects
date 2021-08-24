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
    
    tot_pages = len(corpus.keys())
    out_links = len(corpus[page])
    pdist = dict()

    if out_links == 0:
        pdist = {p: 1/tot_pages for p in corpus}
    else:
        # contribution from randomization
        random_part = (1-damping_factor) * (1/tot_pages)
        for p in corpus:
            pdist[p] = random_part
        
            if p in corpus[page]:
                pdist[p]+= damping_factor * (1/out_links)
        
    return pdist

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    import numpy as np

    # make a dictionary of transition models so we don't have to recompute
    trans_dists = {page: transition_model(corpus, page, damping_factor) for page in corpus}

    # initialize dict for counting the number of times each page appears
    # then randomly choose a starting page and update dict
    sample_record = {page: 0 for page in corpus.keys()}
    
    for i in range(n):
        if i == 0:
            curr_page = np.random.choice(list(corpus.keys()))
        else:
            pdist = trans_dists[curr_page]
            curr_page = np.random.choice(list(corpus.keys()), p = list(pdist.values()))
        sample_record[curr_page]+= 1
    
    return  {page: count/n for page, count in sample_record.items()}

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    import numpy as np

    tot_pages = len(corpus.keys())
    old_vec = np.array([1/tot_pages]*tot_pages)
    trans_dists = {page: transition_model(corpus, page, damping_factor) for page in corpus}

    # Make the transition matrix for the Markov Process
    # This will make the transpose
    MT = []
    for pdist in trans_dists.values():
        MT.append([pdist[page] for page in corpus])

    MT = np.array(MT)
    M = MT.transpose()
    new_vec = M.dot(old_vec)

    while max(new_vec - old_vec) > .001:
        new_vec, old_vec = M.dot(new_vec), new_vec

    res = dict()
    for i, page in enumerate(list(corpus.keys())):
        res[page] = new_vec[i]

    return res


if __name__ == "__main__":
    main()
