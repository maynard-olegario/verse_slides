#!/usr/local/bin/python3
import biblegateway
import slides
import pprint
import re


def main():
    pp = pprint.PrettyPrinter(indent=2)

    citations = get_citations('./verses.txt')
    print('***** AFTER get_citations() *****')
    pp.pprint(citations)

    passages = []
    print('Getting passages ', end='', flush=True)
    for c in citations:
        print('.', end='', flush=True)
        p = get_passage(c['citation'], c['version'])
        passages.append(p)
    print('done', flush=True)

    print('***** AFTER get_passage() *****')
    pp.pprint(passages)

    print('Creating slides ', end='', flush=True)
    for p in passages:
        print('.', end='', flush=True)
        # print('***********')
        # print(p)
        slides.add_slide(str(p['reference']) + ' ' +
                         str(p['version']), p['text'])
    print('done', flush=True)


def get_citations(filename):
    f = open(filename, 'r')
    citations = []
    for line in f:
        version = None
        line = line.strip()

        # get version from end of citation
        matchObj = re.search(
            r'(.*\d+\s*:.*\d+\(*\D*\)*) +([a-zA-Z]+)$', line, re.I)
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

    if version == 'TEV':
        version = 'GNT'
    elif version == 'GNB':
        version = 'GNT'
    elif version == 'God\'s WORD':
        version = 'GW'
    elif version == 'Easy to Read':
        version = 'ERV'
    elif version == 'ETRV':
        version = 'ERV'

    passage = get_common_passages(citation, version)
    if passage != 'empty':
        return passage

    passage = biblegateway.get_passage(
        citation, version, INCLUDE_VERSE, INCLUDE_TITLE)
    if passage == 'empty':
        passage = {'reference': citation, 'version': version,
                   'text': 'Error encountered fetching citation'}
    return passage


def get_common_passages(citation, version):
    # hardcode common verses not easily found online

    # print('citation.lower()=' + citation.lower())
    # print('version.lower()=' + version.lower())

    if citation.lower() == 'acts 20:28' and version.lower() == 'lamsa':
        verse_text = '²⁸Take heed therefore to yourselves and to all the flock, over which the Holy Spirit has appointed you overseers, to feed the church of Christ which he has purchased with his blood.'
    elif citation.lower() == 'john 10:9(a)' and version.lower() == 'reb':
        verse_text = '⁹I am the door; anyone who comes into the fold through me shall be safe. …'
    else:
        verse_text = ''

    if not verse_text:
        return 'empty'
    else:
        passage = {'reference': citation,
                   'version': version,
                   'text': verse_text}
        return passage


if __name__ == '__main__':
    main()
