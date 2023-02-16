.. _sw_overview: 

srsRAN Project Software Architecture
####################################

A primer on the O-RAN gNB architecture has already been outlined in the Knowledge Base, this can be found :ref:`here <oran_gnb_overview>`. This guide aims to 
outline how this architecture is implemented in software, as well as the function of each component and interface.

High Level Architecture
***********************

.. figure:: .imgs/oran_gnb_arch.jpg
    :align: center 
    :class: with-shadow

    O-RAN compliant gNB  of srsRAN Project, showing all main components and interfaces.

srsRAN Project implements all of the components seen in the blue shaded are above, including all relevant interfaces. All of these elements have been implemented in software, and are fully performant, 
customizable and compliant with the O-RAN standard. 3rd-party RICs, RUs, and even gNB components are interoperable with srsRAN Project. 

Components and Interfaces 
==========================

srsRAN Project implements the following components and interfaces:

+-------------+-----------+
| Components  |   Status  |
+=============+===========+
|      DU     | available |
+-------------+-----------+
|    CU-CP    | available |
+-------------+-----------+
|    CU-UP    | available |
+-------------+-----------+

+-----------+-------------+
| Interface |    Status   |
+===========+=============+
|     O1    | implemented |
+-----------+-------------+
|     E1    |             |
+-----------+-------------+
|   E2-du   |   planned   |
+-----------+-------------+
|   E2-cp   |             |
+-----------+-------------+
|   E2-up   |             |
+-----------+-------------+
|    F1-c   |             |
+-----------+-------------+
|    F1-u   |             |
+-----------+-------------+
|     FH    |             |
+-----------+-------------+
|   FAPI+   |             |
+-----------+-------------+
|    NG-c   |             |
+-----------+-------------+
|    NG-u   |             |
+-----------+-------------+
|    XN-c   |             |
+-----------+-------------+
|    XN-u   |             |
+-----------+-------------+

Some modules (SMO, RICs) and interfaces (A1, O2) will be not be implemented as part of srsRAN Project. The modules implemented in srsRAN Project will be compatible with 3rd-party by 
hardware and applications via the interfaces above; this is aligned with the aims of the O-RAN Alliance.

-----

Threading Model
***************

To read more about the Threading Model used for srsRAN Project, you can read :ref:`this section <sw_threading>`.  

-----

Memory Model
************

To read more about the Memory Model used for srsRAN Project, you can read :ref:`this section <sw_memory>`.
