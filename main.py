import biblegateway
import slides

def main():
    citations = get_citations('./verses.txt')
    passages = get_passages(citations)
    print(passages)
    # slides.get_slides()

def get_citations(filename):
    f = open(filename, 'r')
    citations = []
    for line in f:
        citations.append(line)
    return citations

def get_passages(citations):
    default_version = 'NKJV'
    INCLUDE_VERSE = True
    INCLUDE_TITLE = False
    passages = []
    for c in citations:
        p = biblegateway.get_passage(c, default_version, INCLUDE_VERSE, INCLUDE_TITLE)
        passages.append(p)
    return passages

if __name__ == '__main__':
    main()
