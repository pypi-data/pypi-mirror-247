# PyDFT

[![pipeline status](https://gitlab.tue.nl/ifilot/pydft/badges/master/pipeline.svg)](https://gitlab.tue.nl/ifilot/pydft/-/commits/master)
[![Anaconda-Server Badge](https://anaconda.org/ifilot/pydft/badges/version.svg)](https://anaconda.org/ifilot/pydft)
[![Code coverage badge](https://gitlab.tue.nl/ifilot/pydft/badges/master/coverage.svg)](https://gitlab.tue.nl/ifilot/pydft/-/commits/master)
[![PyPI](https://img.shields.io/pypi/v/pydft?color=green)](https://pypi.org/project/pytessel/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Python based Density Functional Theory code for educational purposes. The documentation
of PyDFT can be found [here](https://ifilot.pages.tue.nl/pydft/).

## Purpose

This repository contains a working density functional code using a localized
Gaussian-type basis set and Becke grids for the numerical evaluation
of density functionals.

## Installation

This code depends on a few other packages. To install this code and its
dependencies, run the following one-liner from Anaconda prompt

```bash
conda install -c ifilot pydft pyqint pylebedev pytessel
```

## Usage

### Performing a simple DFT calculation

```python
from pydft import MoleculeBuilder,DFT

#
# Example: Calculate total electronic energy for CO using standard
#          settings.
#

CO = MoleculeBuilder().get_molecule("CO")
dft = DFT(CO, basis='sto3g')
en = dft.scf(1e-4)
print("Total electronic energy: %f Ht" % en)
```

### Visualizing the Becke fuzzy grid

```python
from pydft import MolecularGrid
from pyqint import MoleculeBuilder
import numpy as np
import matplotlib.pyplot as plt

#
# Example: Construct the Becke fuzzy grid and visualize the maximum
#          value of the atomic weight coefficients for a given set of
#          grid points.
#

# construct molecule
mol = MoleculeBuilder().from_name('benzene')
cgfs, atoms = mol.build_basis('sto3g')

# construct molecular grid
molgrid = MolecularGrid(atoms, cgfs)

# produce grid of sampling points to calculate the atomic
# weight coefficients for
N = 150
sz = 8
x = np.linspace(-sz,sz,N)
xv,yv = np.meshgrid(x,x)
points = np.array([[x,y,0] for x,y in zip(xv.flatten(),yv.flatten())])

# calculate the atomic weights
mweights = molgrid.calculate_weights_at_points(points, k=3)

# plot the atomic weights
plt.figure(dpi=144)
plt.imshow(np.max(mweights,axis=0).reshape((N,N)),
           extent=(-sz,sz,-sz,sz), interpolation='bicubic')
plt.xlabel('x [a.u.]')
plt.ylabel('y [a.u.]')
plt.colorbar()
plt.grid(linestyle='--', color='black', alpha=0.5)

# add the atoms to the plot
r = np.zeros((len(atoms), 3))
for i,at in enumerate(atoms):
    r[i] = at[0]
plt.scatter(r[0:6,0], r[0:6,1], s=50.0, color='grey', edgecolor='black')
plt.scatter(r[6:12,0], r[6:12,1], s=50.0, color='white', edgecolor='black')

plt.tight_layout()
```