.. _CU:

CU
#####

As outlined in the Knowledge Base section discussing the :ref:`CU <CU_kb>`, the CU is split into the control plane (CU-CP) and the user plane (CU-UP).
The srsRAN Project CU follows the architecture seen in the Knowledge Base.

CU-CP
*****

As multiple DUs can be connected to the CU-CP, the F1AP, PDCP, and RRC are bundled into the so called DU processor that is created for each connected DU.
Likewise multiple CU-UPs can be connected to the CU-CP, so the E1AP is created inside the CU-UP processor for each connected CU-UP.

**Components:**

    - :ref:`E1AP_cu_cp`: The CU-CP specific implementation of the E1AP
    - :ref:`F1AP_cu`: The CU specific implementation of the F1AP
    - :ref:`PDCP_cu_cp`: Packet Data Convergence Protocol
    - :ref:`RRC_cu`: Radio Resource Control
    - :ref:`NGAP_cu`: The CU specific implementation of the NGAP

**Interfaces:**

    - :ref:`interfaces_E1`: Interface with the CU-UP
    - :ref:`F1-C <interfaces_f1>`: Control plane interface with the DU
    - :ref:`NG-C <interfaces_ng>`: Control plane interface with the Core (AMF)

CU-UP
*****

**Components:**

    - :ref:`E1AP_cu_up`: The CU-UP specific implementation of the E1AP
    - :ref:`F1_U_cu`: The CU-UP specific implementation of the F1-U
    - :ref:`PDCP_cu_up`: Packet Data Convergence Protocol
    - :ref:`SDAP_cu`: Service Data Adaption Protocol
    - :ref:`NG_U_cu`: The CU specific implementation of the NG-U

**Interfaces:**

    - :ref:`interfaces_E1`: Interface with the CU-CP
    - :ref:`F1-U <interfaces_f1>` User plane interface with the DU
    - :ref:`NG-U <interfaces_ng>` User plane interface with the Core (AMF)

-----

.. toctree::
   :maxdepth: 1
