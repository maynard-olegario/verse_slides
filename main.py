#!/usr/local/bin/python3
import biblegateway
import slides
import pprint
import re

def main():
    pp = pprint.PrettyPrinter(indent=2)

    citations = get_citations('./verses.txt')
    print('***** AFTER get_citations() *****')
    pp.pprint (citations)

    passages = []
    for c in citations:
        p = get_passage(c['citation'], c['version'])
        passages.append(p)

    print('***** AFTER get_passage() *****')
    pp.pprint (passages)

    for p in passages:
        # print('***********')
        # print(p)
        slides.add_slide(str(p['reference']) + ' ' + str(p['version']), p['text'])

def get_citations(filename):
    f = open(filename, 'r')
    citations = []
    for line in f:
        version = None
        line = line.strip()

        # get version from end of citation
        matchObj = re.search( r'(.*\d+\s*:.*\d+) *([a-zA-Z]+)$', line, re.I)
        if matchObj:
            book_chap_verse = matchObj.group(1)
            version = matchObj.group(2)
        else:
            book_chap_verse = line
            version = ''
        citation = {'citation': book_chap_verse, 'version': version}
        citations.append(citation)
    return citations

def get_passage(citation, version='NKJV'):
    INCLUDE_VERSE = True
    INCLUDE_TITLE = False
    # print('citation=' + str(citation) + ' :: version=' + str(version))

    if version == '':
        version = 'NKJV'
    elif version == 'TEV':
        version = 'GNT'
    elif version == 'GNB':
        version = 'GNT'
    elif version == 'God\'s WORD':
        version = 'GW'
    elif version == 'Easy to Read':
        version = 'ERV'
    elif version == 'ETRV':
        version = 'ERV'

    passage = biblegateway.get_passage(citation, version, INCLUDE_VERSE, INCLUDE_TITLE)
    if passage == 'empty':
        passage = {'reference': citation, 'version': '', 'text': 'Error encountered fetching citation'}
    return passage

if __name__ == '__main__':
    main()
