.. _cohp_analysis:
.. index:: cohpanalysis

.. note::

    All the code examples listed below reside in the :code:`examples` folder and
    act on data files which can be found in the
    :code:`samples` folder. If you cloned the repository, you should be able to
    directly use them from the :code:`examples` folder.

COHP Analysis
=============

Getting started
---------------

:program:`QuantumSculpt` can perform analysis on DOS files via 
the :code:`CrystalOrbitalHamiltonPopulation` class and the plotting 
routines as part of the :code:`quantumsculpt` module. The procedure is very much
akin to the procedure used to create density of states plots, though there are a
number of subtle though important differences.

To parse the contents of a :code:`COHPCAR.lobster` file, we execute the following

.. code:: python

    import os
    import matplotlib.pyplot as plt
    from quantumsculpt import CrystalOrbitalHamiltonPopulation
    import quantumsculpt as qs

    # load the COHPCAR.lobster file via a CrystalOrbitalHamiltonPopulation class
    ROOT = os.path.dirname(__file__)
    filename = os.path.join(ROOT, '..', '..', 'samples', 'carbonmonoxide_gasphase', 'pbe', 'COHPCAR.lobster')
    cohp = CrystalOrbitalHamiltonPopulation(filename)

The object :code:`cohp` contains the complete contents of the :code:`COHPCAR.lobster` file and can be used
for retrieval of specific data as well as for visualization. For example, to retrieve the energies and
the total averaged COHP, we can use the following

.. code:: python

    print(len(cohp.get_dataitems()))
    energies = cohp.get_energies()
    print(energies.shape, energies[0], energies[-1])
    avgcohp = cohp.get_dataitem(0)
    print(avgcohp.keys())
    print(avgcohp['type'])

The output of the above code is::

    18
    (801,) -30.03755 10.01252
    dict_keys(['type', 'label', 'cohp', 'icohp'])
    average

This output essentially tells us that the :code:`COHPCAR.lobster` file contains 18 data items and has
801 data points between the energy interval :math:`E \in (-30.03755, 10.01252)`. The function :code:`get_dataitem(0)` 
retrieves the first data item which always corresponds to the averaged COHP. Every data item is essentially
a dictionary containing four key,value pairs

* :code:`type`: Type of the interaction, e.g. :code:`average`, :code:`orbitalwise`, or :code:`total`
* :code:`label`: Label identifying the interaction
* :code:`cohp`: Numpy array containing the COHP values
* :code:`icohp`: Numpy array containing the integrated COHP values

To get a quick overview of the contents of a COHP object, you can readily print is

.. code:: python

    print(cohp)

which yields the following results::

    Filename: d:\programming\python\quantumsculpt\examples\cohp\..\..\samples\carbonmonoxide_gasphase\pbe\COHPCAR.lobster
    Data items:
        average: Average
        total: O2->C1
        orbitalwise: O2[2s]->C1[2s]
        orbitalwise: O2[2p_y]->C1[2s]
        orbitalwise: O2[2p_z]->C1[2s]
        orbitalwise: O2[2p_x]->C1[2s]
        orbitalwise: O2[2s]->C1[2p_y]
        orbitalwise: O2[2p_y]->C1[2p_y]
        orbitalwise: O2[2p_z]->C1[2p_y]
        orbitalwise: O2[2p_x]->C1[2p_y]
        orbitalwise: O2[2s]->C1[2p_z]
        orbitalwise: O2[2p_y]->C1[2p_z]
        orbitalwise: O2[2p_z]->C1[2p_z]
        orbitalwise: O2[2p_x]->C1[2p_z]
        orbitalwise: O2[2s]->C1[2p_x]
        orbitalwise: O2[2p_y]->C1[2p_x]
        orbitalwise: O2[2p_z]->C1[2p_x]
        orbitalwise: O2[2p_x]->C1[2p_x]
        Energy interval: (-30.0375, 10.0125)
        Number of data points: 801

.. note::

    The path to the filename is not sanitized.

For a COHP file, there is a single convenience function to plot the averaged COHP.

.. code:: python

    fig, ax = plt.subplots(1,1, dpi=144)
    qs.plot_averaged_cohp(ax, 
                        cohp, 
                        icohp=True, 
                        grid=True,
                        ylim=(-30,5))

which produces a plot such as seen below.

.. figure:: ../_static/img/cohp/cohp00.png

Decompositions and collections
------------------------------

Partial integration
-------------------