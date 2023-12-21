import numpy as np

from .helpers import parse_filelines


class Output():
    """
    container for NUIT Output file.    
    """

    def __init__(self, filepath):
        with open(filepath) as fileopen:
            self.filelines = fileopen.readlines()
        try:  # to avoid diffenrence between print_all_steps=0/1
            self._read_burnups()
            self._read_powers()
            self._read_timesteps()
            self._read_fluxes()
        except:
            pass
        self._read_isotopes()

    def _read_isotopes(self):
        self.nuclide_masses = []
        index = parse_filelines(self.filelines, 'Nuclide Density', 0) + 1
        index = parse_filelines(self.filelines, 'NucID', index) + 2
        while "Non-Actinide" not in self.filelines[index]:
            line = self.filelines[index].split()
            nuc_id, nuc_name = int(line[0]), line[1]
            nuc_den = np.asarray([float(item) for item in line[2:]])
            self.nuclide_masses.append({'nucid': nuc_id,
                                        'name': nuc_name,
                                        'data': nuc_den})
            index += 1

    def _read_burnups(self):
        self.burnups = []
        ind = parse_filelines(self.filelines, 'BU(MWd/kgHM):', 0)
        line = self.filelines[ind].split()
        for bu in line[1:]:
            self.burnups.append(float(bu))
        self.burnups = np.asarray(self.burnups)

    def _read_powers(self):
        self.powers = []
        ind = parse_filelines(self.filelines, 'Power(MW):', 0)
        line = self.filelines[ind].split()
        for pw in line[1:]:
            self.powers.append(float(pw))
        self.powers = np.asarray(self.powers)

    def _read_timesteps(self):
        self.timesteps = []
        ind = parse_filelines(self.filelines, 'TotalTime(s):', 0)
        line = self.filelines[ind].split()
        for ts in line[1:]:
            self.timesteps.append(float(ts))
        self.timesteps = np.asarray(self.timesteps)

    def _read_fluxes(self):
        self.fluxes = []
        ind = parse_filelines(self.filelines, 'Flux(n/cm^2/s):', 0)
        line = self.filelines[ind].split()
        for fl in line[1:]:
            self.fluxes.append(float(fl))
        self.fluxes = np.asarray(self.fluxes)

    def match(self, key='name', value='Cs137', type='nuclide'):
        """
        Match an element from stored tables using key-value pair.
        """
        if type == 'nuclide':
            table = self.nuclide_masses
        elif type == 'burnup':
            table = self.burnups
        nuclide = next((item for item in table if item[key] == value), None)
        return nuclide

    def get_nuclide_mass(self, nuclide: str, burnup: float = None):
        """"
        Get nuclide mass at a certain burnup depth.
        """
        if burnup:
            return self.match('name', nuclide, 'nuclide')[abs(self.burnups-burnup).argmin()]
        else:
            return self.match('name', nuclide)['data']

    def output_nuclide_mass(self, nuclide_list, burnup=None):
        """
        Get nuclide mass in batch.
        """
        return [self.get_nuclide_mass(nuclide, burnup) for nuclide in nuclide_list]
