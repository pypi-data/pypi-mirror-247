import unittest
import numpy as np
import sys
import os

# add a reference to load the module
ROOT = os.path.dirname(__file__)
sys.path.append(os.path.join(ROOT, '..'))

from quantumsculpt import DensityOfStates

class TestDOS(unittest.TestCase):

    def test_read_doscar(self):
        filename = os.path.join(ROOT, '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'DOSCAR.lobster')
        dos = DensityOfStates(filename)
        
        self.assertEqual(dos.get_nr_atoms(), 2)
        self.assertEqual(dos.get_npts(), 801)
    
        # check integrity of total DOS
        total_dos = dos.get_total_dos()
        keys = ('energies', 'states','istates')
        for key in keys:
            self.assertTrue(key in total_dos, msg='No %s found' % key)
        self.assertEqual(len(total_dos['energies']), 801)

        dos_atom = dos.get_dos_atom(1)
        keys = ('states', 'atomid', 'atomnumber', 'labels')
        for key in keys:
            self.assertTrue(key in dos_atom)
        self.assertEqual(dos_atom['atomnumber'], 6)
        self.assertEqual(dos_atom['atomid'], 1)
        self.assertEqual(len(dos_atom['labels']), 4)
        
        dos_atom = dos.get_dos_atom(2)
        keys = ('states', 'atomid', 'atomnumber', 'labels')
        for key in keys:
            self.assertTrue(key in dos_atom)
        self.assertEqual(dos_atom['atomnumber'], 8)
        self.assertEqual(dos_atom['atomid'], 2)
        self.assertEqual(len(dos_atom['labels']), 4)
        
        keys = ('states', 'label')
        for key in keys:
            self.assertTrue(key in dos_atom['states'][0], msg='No %s found' % key)

if __name__ == '__main__':
    unittest.main()
