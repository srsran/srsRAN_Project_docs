.. _du_overview: 

DU
##


As outlined in the Knowledge Base section discussing the :ref:`DU <DU_kb>`, there are two main components to the DU: the DU-high and DU-low. 

The srsRAN Project DU follows the architecture seen in the Knowledge Base, with the addition of the DU Manager. This results in the DU having the following architecture: 

.. figure:: .imgs/du.png
   :scale: 60%
   :alt: DU Architecture
   :align: center

From this we can clearly see how the DU is split into the DU-high and DU-low, with the following main components and interfaces: 

**Components:**

    - DU Manager: This is an srsRAN Project specific component and implementation
    - F1AP-DU: The DU specific implementation of the F1AP
    - RLC: Radio Link Control
    - MAC: Medium Access Control 

**Interfaces:**

    - E2: Interfaces with the nRT RIC
    - F1-c: Interfaces with the CU control plane 
    - F1-u: Interfaces with the CU user plane
    - FAPI: Interface between the DU-high and DU-low 
   
.. note::
   These are discussed in detail in the Interfaces section 

-----

DU-High
*******

.. toctree::
   :maxdepth: 1
   
   DU_high/du_manager.rst
   DU_high/F1AP_du.rst
   DU_high/rlc.rst
   DU_high/mac.rst

-----

DU-Low
******

Documentation discussing the implementation of the DU-low and its components can be found :ref:`here <DU_low>`. 

