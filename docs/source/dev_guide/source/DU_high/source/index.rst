.. _du_high: 

DU-high
#######

.. figure:: .imgs/DU_high.png
   :scale: 60%
   :align: center

   srsRAN Project DU-high implementation


**Components:**

    - :ref:`DU Manager <DU_manager>`: This is an srsRAN Project specific component and implementation which is responsible for managing the DU, specifically the connected UEs and RAN Resources. 
    - :ref:`RLC <rlc_overview>`: The Radio Link Control (RLC) layer sits between the MAC in the DU-high and the F1AP/PDCP in the CU, and provides the transport services for SRBs and PRBs between these layers. It operates in three modes: transparent, unacknowledged and acknowledged. 
    - :ref:`MAC <mac>`: The Medium Access Control (MAC) is responsible for the encoding and decoding of MAC PDUs, scheduling uplink and downlink grants and other control services. 

**Interfaces:**

    - :ref:`E2 <E2AP_du_high>`: Interfaces with the nRT RIC.
    - :ref:`F1 <F1AP_du_high>`: Interfaces with the CU control and user plane.
    - :ref:`FAPI <FAPI_high>`: Interface between the DU-high and DU-low.

-----

**Contents:**

.. toctree::
   :maxdepth: 1
   
   du_manager.rst
   rlc.rst
   mac.rst
   E2AP_du_high.rst
   F1AP_du_high.rst
   FAPI_high.rst


