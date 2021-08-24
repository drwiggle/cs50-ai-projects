import nltk
import numpy
import string
import os
import sys

FILE_MATCHES = 1
SENTENCE_MATCHES = 1
STOP_WORDS = nltk.corpus.stopwords.words("english")
PUNCTUATION = string.punctuation

def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)
    
    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """



    filecontents = dict()
    for filename in os.listdir(directory):
        if filename[-4:] == ".txt":
            fullpath = os.path.join(directory, filename)
            with open(fullpath, encoding = 'utf-8', errors='ignore') as f:
                contents = f.read()
                filecontents[filename] = contents
    return filecontents


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    
    # Lower entire document and tokenize words
    document = document.lower()
    messy_words = nltk.word_tokenize(document)

    # Make a dictionary whose keys are punctuation and all of whose values
    # are None.  Make a list of stopwords

    translate_table = dict((ord(char), None) for char in PUNCTUATION)

    # Process list of messy_words
    words = []
    for word in messy_words:
        if word == "n't":
            word = 'not'
        word = word.translate(translate_table)
        if len(word) > 0 and word not in STOP_WORDS:
            words.append(word)

    return words



def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    
    num_docs = len(documents.keys())
    
    allwords = set()
    for wordlist in documents.values():
        allwords = allwords.union(set(wordlist))

    idfs = dict()
    for word in allwords:
        doc_count = sum([1 if word in doc_words else 0
        for doc_name, doc_words in documents.items()
        ])
        idfs[word] = numpy.log(num_docs/doc_count)

    return idfs

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """

    tf_idfs = dict()
    for f, wordlist in files.items():
        idfvals = []
        for word in query:
            if word in idfs:
                idfvals.append(wordlist.count(word) * idfs[word])
        tf_idfs[f] = sum(idfvals)

    sortedfiles = sorted(tf_idfs.keys(), key = lambda f: tf_idfs[f], reverse= True)
    numfiles = len(sortedfiles)
    
    return sortedfiles[:min(n, numfiles)]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    s_ranks = dict()
    for s, s_words in sentences.items():
        q_word_idfs = []
        for word in query:
            if word in s_words:
                q_word_idfs.append(idfs[word])
                
        s_rank = sum(q_word_idfs)
        qtd = sum([w in query for w in s_words])/len(s_words)
        s_ranks[s] = (s_rank, qtd)

    # with open('output.txt', 'w', encoding = 'utf-8') as f:
    #     print('{\n')
    #     for s, rank in s_ranks.items():
    #         print(f'{s}: {rank}\n' )
    #     print('}')
    
    sortedsents = sorted(s_ranks.keys(), key = lambda s: s_ranks[s], reverse = True)
    numsents = len(sortedsents)
    
    return sortedsents[:min(n, numsents)]


if __name__ == "__main__":
    main()
