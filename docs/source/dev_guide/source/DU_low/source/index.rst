.. _du_low: 

DU-low
######

.. figure:: .imgs/DU_low.png
   :scale: 60%
   :align: center

   srsRAN Project DU-low implementation

**Components:**

    - :ref:`Upper PHY <upper_phy>`: The Upper PHY handles the processing of UL and DL signals coming from and to the RU. 

**Interfaces:**

    - :ref:`FAPI <FAPI_low>`: Interfaces with the MAC in the DU-high.
    - :ref:`OFH <ofh>`: Interfaces with the lower PHY in the Radio Unit (RU).

-----

**Contents:**

.. toctree::
   :maxdepth: 1
   
   upper_phy.rst
   FAPI_low.rst
   ofh.rst


