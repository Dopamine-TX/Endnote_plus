#!/usr/bin/env python

import sys
import glob
import os
import pandas as pd

import difflib

import pybktree
import editdistance

from xml_parser import parse_exported_xml


def jterm_distance(a, b):
    return editdistance.eval(a.lower(), b.lower())

class JournalNameRegulator(object):

    def __init__(self):
        self._fullname_bktree_ = pybktree.BKTree(distance_func=jterm_distance)
        self._abbr_bktree_ = pybktree.BKTree(distance_func=jterm_distance)


    def _std_jname_validation(self, std_journal_name, journal_name):
        """ validate if a name in the dictionary is suitable """
        dr = difflib.ndiff(std_journal_name, journal_name)
        diff = [d[2] for d in dr if d[0] != " "]
        if any([c.isalpha() for c in diff]):
            return False
        else:
            return True


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
        found = full_tree.find(journal_name, 20)
        if not found:
            return "!! not found"

        dist, std_journal_name = found[0]
        if dist == 0:
            if std_journal_name != journal_name:
                return "+ " + std_journal_name
            else:
                return "--same--"

        elif dist > 3:
            return "! " + str(dist) + " " + std_journal_name

        if self._std_jname_validation(std_journal_name, journal_name):
            return "- " + std_journal_name
        else:
            return "! " + str(dist) + " " + std_journal_name


def test():
    jr = JournalNameRegulator()
    #jr.read_database(sys.argv[1])
    jr.read_database("termlist")
    #jnames_testset = parse_exported_xml("data/ws-Saved-Converted.xml")
    jnames_testset = parse_exported_xml("data/Biomaterials-2021.xml")
    jnames_testset = set(jnames_testset)
    print(len(jnames_testset))

    for jname in jnames_testset:
        print(jname)
        print(jr.regulate(jname))
        print()

if __name__ == "__main__":
    test()

