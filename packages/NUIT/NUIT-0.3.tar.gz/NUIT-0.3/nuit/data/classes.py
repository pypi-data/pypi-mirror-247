
from typing import List, Union, Any
from functools import cached_property
from ..constants import MT_dict
from ..helpers import decompose_nucname


class Reaction():

    def __init__(self, name: str, data: dict):
        self.name = name
        self.data = data

    @cached_property
    def MT(self):
        return MT_dict[self.name]

    def __repr__(self):
        return self.name

    def __getattr__(self, attr: str):
        if attr in self.data:
            return self.data[attr]
        else:
            return None


class Nuclide(list):

    def __init__(self, name: str, reaction: List[Reaction] = [], data: dict = None):
        self.name = name
        self.data = data
        super().__init__(reaction)

    def __repr__(self):
        return self.name

    @cached_property
    def nucid(self):
        return decompose_nucname(self.name)["nucid"]

    @property
    def num_rec(self):
        return len(self)

    def __call__(self, reaction: Union[str, int]):
        rec_index = 'name' if isinstance(reaction, str) else 'MT'
        return next(reactioni for reactioni in self if getattr(reactioni, rec_index) == reaction)

    def sort_reactions(self):
        self.sort(key=lambda reaction: reaction.MT)


class Nuclib(list):

    def __init__(self, type: str, nuclides: List[Nuclide] = []):
        self.type = type
        super().__init__(nuclides)

    def __call__(self, nuclide: Union[str, int]):
        """
        Returns the first instance of a nuclide in the class that matches the given nuclide name or ID.

        Parameters:
        - nuclide: A string representing the name of the nuclide or an integer representing the nuclide ID.

        Returns:
        - The first instance of the nuclide found in the class.

        Raises:
        - StopIteration: If no matching nuclide is found in the class.
        """
        nuc_index = 'name' if isinstance(nuclide, str) else 'nucid'
        return next(nuclidei for nuclidei in self if getattr(nuclidei, nuc_index) == nuclide)

    def sort_nuclides(self):
        self.sort(key=lambda nuclide: nuclide.nucid)
