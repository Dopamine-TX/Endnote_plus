import sys
import glob
import os
import pandas as pd

import pybktree
import editdistance


def jterm_distance(a, b):
    return editdistance.eval(a.lower(), b.lower())

class JournalNameRegulator(object):

    def __init__(self):
        self._fullname_bktree_ = pybktree.BKTree(distance_func=jterm_distance)
        self._abbr_bktree_ = pybktree.BKTree(distance_func=jterm_distance)


    def read_database(self, journal_termlist_dir):
        """ read journal name database """
        full_tree = self._fullname_bktree_
        abbr_tree = self._abbr_bktree_

        termlist_filenames = glob.glob(os.path.join(journal_termlist_dir, "*.txt"))
        for filename in termlist_filenames:
            print("reading", filename)
            df = pd.read_csv(filename, delimiter="\t", names=("full_name", "abbr1", "abbr2", "abbr3"))
            for term in df["full_name"]:
                full_tree.add(term)


    def regulate(self, journal_name):
        full_tree = self._fullname_bktree_
        return full_tree.find(journal_name, 3)[0]


def test():
    jr = JournalNameRegulator()
    jr.read_database(sys.argv[1])
    print(jr.regulate("Nature"))

if __name__ == "__main__":
    test()

