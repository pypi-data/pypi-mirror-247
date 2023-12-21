import platform
import time
import subprocess
import xml.etree.ElementTree as et
import xml.dom.minidom as mdm

from re import match as re_match

from typing import Literal, List

from . import constants
from . import output


class Model(et.ElementTree):

    def __init__(self, filepath: str = None):
        super().__init__(element=et.Element('input'))
        self._root = self.getroot()
        if filepath is not None:
            self.parse(filepath)

    def remove_node(self, node_name: str):
        """
        Removes a node from the tree.

        Args:
            node_name (str): The name of the node to be removed.

        Returns:
            None
        """
        if (node := self._root.find(node_name)) is not None:
            self._root.remove(node)

    def set_library(self,
                    lib_path: str,
                    sub_xs_lib: str = None,
                    only_use_endf_data: bool = False,
                    xs_lib: str = None,
                    ):
        """
        Sets the library information for the model.

        Parameters:
        - lib_path (str): The path to the library.
        - sub_xs_lib (str, optional): The path to the sub XS library. Defaults to None.
        - only_use_endf_data (bool, optional): Flag indicating whether to only use ENDF data. Defaults to False.
        - xs_lib (str, optional): The path to the XS library. Defaults to None.
        """
        # remove the existing library node
        if (node := self._root.find('library')) is not None:
            self._root.remove(node)

        # collect all the input information
        info = {'lib_path': str(lib_path),
                'only_use_endf_data': str(only_use_endf_data)}
        if sub_xs_lib:
            info['sub_xs_lib'] = str(sub_xs_lib)
        if xs_lib:
            info['xs_lib'] = str(xs_lib)
        et.SubElement(self._root, 'library', info)

    def add_nuclide(self,
                    name: str,
                    den: float,
                    unit: Literal['gram', 'barn'] = 'gram'):
        """
        Add a nuclide to the material.

        Args:
            name (str): The name of the nuclide.
            den (float): The density of the nuclide.
            unit (Literal['gram', 'barn'], optional): The unit of the density. Defaults to 'gram'.

        Returns:
            None
        """

        # add the material node if it does not exist
        if self._root.find('material') is None:
            et.SubElement(self._root, 'material', {'unit': unit})
        material = self._root.find('material')

        # input validity check
        if material.attrib['unit'] != unit:
            raise ValueError('Unit of material is not consistent.')

        # add the nuclide node
        mres = re_match(r'([A-z]*)(\d*)([m]?)', name)
        name, mass, status = mres.groups()
        status = 1 if status == 'm' else 0
        A = constants.Atomic_list.index(name)+1
        id = int(A)*10000+int(mass)*10 + status

        # collect all the input information
        info = {'den': str(den), 'id': str(id)}
        et.SubElement(material, 'nuc', info)

    def add_burnup(self,
                       time: float,
                       val: float,
                       repeat: int = 1,
                       mode: Literal['constpower', 'constflux', 'decay'] = 'constpower',
                       unit: Literal['day', 'hour', 'minute', 'second'] = 'day',
                       spectrum: List[float] = None):
            """
            Adds a burnup node to the XML tree.

            Usage:
            - Adds a burnup node with the specified time, value, and other optional parameters to the XML tree.

            Args:
            - time (float): The time value for the burnup node.
            - val (float): The value for the burnup node (power or flux).
            - repeat (int, optional): The number of times to repeat the burnup node (default: 1).
            - mode (Literal['constpower', 'constflux', 'decay'], optional): The mode of the burnup node (default: 'constpower').
            - unit (Literal['day', 'hour', 'minute', 'second'], optional): The unit of the time value (default: 'day').
            - spectrum (List[float], optional): The spectrum values for the burnup node (default: None).

            Returns:
            - None
            """
            # add the burnup node if it does not exist
            if self._root.find('burnup') is None:
                et.SubElement(self._root, 'burnup', {})
            burnup = self._root.find('burnup')

            # input validity check
            if unit not in ['day', 'hour', 'minute', 'second']:
                raise KeyError('Time unit should be day, hour, minute or second.')
            if mode not in ['constpower', 'constflux', 'decay']:
                raise KeyError('Power mode should be constpower, constflux or decay.')

            # add the burn node
            # collect all the input information
            val_name = 'power' if mode == 'constpower' else 'flux'
            info = {'time': str(time), 'unit': unit,
                    'mode': mode, val_name: str(val),
                    'repeat': str(repeat)}
            burnup_node = et.SubElement(burnup, 'burn', info)

            # add the spectrum if necessary
            if spectrum is not None:
                spectrum = ' '.join([f"{s:8.3e}" for s in spectrum])
                burnup_node.set('spectrum', spectrum)


    # def set_gen_library(self,
    #                     flux_spectrum,
    #                     temperature,
    #                     energy_boundary,
    #                     data_path,
    #                     decay_file='decay',
    #                     neutron_file='neutron',
    #                     nfy_file='nfy',
    #                     output_path='NUITLIB'):

    #     print("Method deprecated!")

    #     # modify the flux_spectrum into str
    #     flux_spectrum = ' '.join([str(s) for s in flux_spectrum])
    #     if energy_boundary[0] < 1E-6:
    #         energy_boundary += 1E-6
    #     energy_boundary = ' '.join([str(s) for s in energy_boundary])

    #     # remove the existing library node
    #     if (node := self._root.find('gen_library')) is not None:
    #         self._root.remove(node)

    #     info = {}
    #     for item in ['flux_spectrum', 'temperature', 'energy_boundary',
    #                  'data_path', 'decay_file', 'neutron_file', 'nfy_file', 'output_path']:
    #         if locals()[item] is not None:
    #             info[item] = str(locals()[item])
    #     et.SubElement(self._root, 'gen_library', info)

    def set_output(self,
                   type: Literal['isotope', 'gammaspectra', 'absorption', 'fission', 'decayheat',
                                 'decayheat-lp', 'decayheat-em', 'decayheat-hp', 'radioactivity', 'betaspectra'],
                   print_all_step: bool = True,
                   integral: bool = False):
        """
        Usage: Set the type of output, whether to print all steps, and whether to calculate the integral.

        Args:
        - type (Literal['isotope', 'gammaspectra', 'absorption', 'fission', 'decayheat',
                        'decayheat-lp', 'decayheat-em', 'decayheat-hp', 'radioactivity', 'betaspectra']):
            The type of output.
        - print_all_step (bool):
            Whether to print all steps. Default is True.
        - integral (bool):
            Whether to calculate the integral. Default is False.

        Returns:
        - None
        """
        # add the output node if it does not exist
        if self._root.find('output') is None:
            et.SubElement(self._root, 'output', {})
        output = self._root.find('output')

        # input validity check
        if type not in ['isotope', 'gammaspectra', 'absorption', 'fission', 'decayheat',
                        'decayheat-lp', 'decayheat-em', 'decayheat-hp', 'radioactivity', 'betaspectra']:
            raise KeyError('Not a valid output type.')

        # add the output node
        # collect all the input information
        info = {'type': type,
                'print_all_step': str(int(print_all_step)),
                'integral': str(int(integral))}
        et.SubElement(output, 'table', info)

    def export_to_xml(self, filepath: str):
        """
        Export the object to an XML file.

        Args:
            filepath (str): The path to the XML file.

        Returns:
            None
        """
        super().write(file_or_filename=filepath)

        # additional process to make the xml file pretty
        dom = mdm.parse(filepath)
        pdom = dom.toprettyxml(indent='\t', newl='\n')
        dom.unlink()
        with open(filepath, 'w') as fileopen:
            fileopen.write(pdom)

    def __call__(self, filepath: str, nuitpath: str):
        self.export_to_xml(filepath)
        print(f"Running NUIT...\n|-Executable:{nuitpath}\n|-Input:{filepath}\n|-Output:{filepath+'.out'}\n|-Time:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
        if platform.system() == 'Windows':
            out = subprocess.Popen(f"{nuitpath} -i {filepath}",
                                     shell=True,
                                     stdout=subprocess.PIPE).communicate()
        else:
            out = subprocess.Popen(f"wine {nuitpath} -i {filepath}",
                                    shell=True,
                                    stdout=subprocess.PIPE).communicate()
        with open(filepath+'.log', 'w') as fileopen:
            fileopen.write(out[0].decode())
        return output.Output(filepath+'.out')
