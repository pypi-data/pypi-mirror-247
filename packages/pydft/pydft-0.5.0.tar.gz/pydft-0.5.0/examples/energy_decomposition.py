import os,sys
import numpy as np

# add a reference to load the module
ROOT = os.path.dirname(__file__)
sys.path.insert(1, os.path.join(ROOT, '..'))

from pydft import MoleculeBuilder, DFT

co = MoleculeBuilder().from_name("CO")
dft = DFT(co, basis='sto3g', verbose=True)
en = dft.scf(1e-4)
print("Total electronic energy: %f Ht" % en)

# retrieve molecular matrices
res = dft.get_data()
P = res['P']
T = res['T']
V = res['V']
J = res['J']

# calculate energy terms
Et = np.einsum('ji,ij', P, T)
Ev = np.einsum('ji,ij', P, V)
Ej = 0.5 * np.einsum('ji,ij', P, J)
Ex = res['Ex']
Ec = res['Ec']
Exc = res['Exc']
Enuc = res['enucrep']

print('Kinetic energy:              %12.6f' % Et)
print('Nuclear attraction:          %12.6f' % Ev)
print('Electron-electron repulsion: %12.6f' % Ej)
print('Exchange energy:             %12.6f' % (Ex))
print('Correlation energy:          %12.6f' % (Ec))
print('Exchange-correlation energy: %12.6f' % (Exc))
print('Nucleus-nucleus repulsion:   %12.6f' % (Enuc))

print('Sum: %12.6f' % (Et + Ev + Ej + Exc + Enuc))