.. _du_low: 

DU-low
######

.. figure:: .imgs/DU_low.png
   :scale: 60%
   :align: center

   srsRAN Project DU-low implementation

:ref:`Back to top level architecture diagram <sw_overview>`.

**Components:**

    - Upper PHY: The Upper PHY handles the processing of UL and DL signals coming from and to the RU. 

.. :ref:`Upper PHY <upper_phy>`: The Upper PHY handles the processing of UL and DL signals coming from and to the RU.

**Interfaces:**


    - FAPI: Interfaces with the MAC in the DU-high.
    - OFH: Interfaces with the lower PHY in the Radio Unit (RU).

.. :ref:`FAPI <FAPI_low>`: Interfaces with the MAC in the DU-high.
.. :ref:`OFH <ofh>`: Interfaces with the lower PHY in the Radio Unit (RU).

-----

.. Add TOCTREE here once pages or populated


