from pickle import load
from collections import namedtuple
from typing import Union


ISOclause = namedtuple("ISOclause", ["nucname", "MT", "fracm"])


class ISOlib():

    def __init__(self, clauses):
        self.clauses = clauses

    def __call__(self, nuclide: Union[str, int], reaction: Union[str, int]):
        nuc_index = 'nucname' if isinstance(nuclide, str) else 'nucid'
        rec_index = 'recname' if isinstance(reaction, str) else 'MT'
        clause = next((clause for clause in self.clauses if clause[nuc_index] == nuclide and clause[rec_index] == reaction))
        return clause

    @classmethod
    def from_pickle(cls, filepath: str):
        isolib = ISOlib()
        with open(filepath, 'rb') as fileopen:
            isomerics = load(fileopen)
        isolib.clauses = [ISOclause(iso["name"], iso["MT"], iso["fracm"]) for iso in isomerics]
        return isolib
