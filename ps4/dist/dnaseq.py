#!/usr/bin/env python2.7

import unittest
import kfasta 
from dnaseqlib import * 
from itertools import tee
import sys

### Utility classes ###

# Maps integer keys to a set of arbitrary values.


class Multidict:
    # Initializes a new multi-value dictionary, and adds any key-value
    # 2-tuples in the iterable sequence pairs to the data structure.
    def __init__(self, pairs=[]):
        self.multi_dict = {}
      # Associates the value v with the key k.

    def items(self):
        return self.multi_dict.items()

    def put(self, k, v):
        if(self.multi_dict.get(k) is None):
            self.multi_dict.update({k: [v]})
        else:
            self.multi_dict[k].append(v)
    # Gets any values that have been associated with the key k; or, if
    # none have been, returns an empty sequence.

    def __str__(self):
        return str(self.multi_dict)

    def get(self, k):
        value = self.multi_dict.get(k)
        if(value is None):
            return []
        else:
            return value

# Given a sequence of nucleotides, return all k-length subsequences
# and their hashes.  (What else do you need to know about each
# subsequence?)


def subsequenceHashes(seq, k):
    subsequences = kfasta.subsequences(seq, k)
    new_subsequence = subsequences.next()
    subseqHash = RollingHash(new_subsequence)
    pos = 0
    try:
        while True:
            yield (pos, new_subsequence, subseqHash.current_hash())
            prev_item = new_subsequence[0]
            new_subsequence = subsequences.next()
            subseqHash.slide(prev_item, new_subsequence[k-1])
            pos += 1
    except StopIteration:
        return

# Similar to subsequenceHashes(), but returns one k-length subsequence
# every m nucleotides.  (This will be useful when you try to use two
# whole data files.)


def intervalSubsequenceHashes(seq, k, m):
    pos = 0
    try:
        while True:
            subseq = ''
            while len(subseq)< k:
                subseq += seq.next()
            subseqHash = RollingHash(subseq)
            yield (pos, subseq, subseqHash.current_hash()) 
            for _ in range(0, m-k):
                seq.next()
            pos += m
    except StopIteration:
        return


# Searches for commonalities between sequences a and b by comparing
# subsequences of length k.  The sequences a and b should be iterators
# that return nucleotides.  The table is built by computing one hash
# every m nucleotides (for m >= k).
def getExactSubmatches(a, b, k, m):
    a_subseq_hash = intervalSubsequenceHashes(a, k, m)
    b_subseq_hash = subsequenceHashes(b, k)
 
    multi_dict = Multidict()
    print("Building Table from Sequence A")
    for pos, subseq , a_hash in a_subseq_hash:
        multi_dict.put(a_hash, (pos, subseq))
    print("Matching Sequence B")
    for pos, subseq, b_hash in b_subseq_hash:
        value = multi_dict.get(b_hash)
        if(len(value)):
            for a_pos, a_subseq in value:
                if(subseq == a_subseq):
                    yield (a_pos, pos)                            

if __name__ == '__main__':
    #print(list(getExactSubmatches(iter('yabcabcabcz'), iter('xxabcxxxx'), 3, 1)))
    if len(sys.argv) != 4:
       print 'Usage: {0} [file_a.fa] [file_b.fa] [output.png]'.format(sys.argv[0])
       sys.exit(1)
    #The arguments are, in order: 1) Your getExactSubmatches
    #function, 2) the filename to which the image should be written,
    #3) a tuple giving the width and height of the image, 4) the
    #filename of sequence A, 5) the filename of sequence B, 6) k, the
    #subsequence size, and 7) m, the sampling interval for sequence
    #A.
    compareSequences(getExactSubmatches,
                   sys.argv[3], (500, 500), sys.argv[1], sys.argv[2], 8, 100)
