.. _CU_cp:

CU-CP
#####

.. figure:: .imgs/CU_CP.png
    :align: center 
    :width: 40%

    srsRAN Project CU-CP implementation. 

The CU-CP, or Central Unit - Control Plane, is the responsible for the handling of control plane messaging. Specifically the control plane part of the PDCP protocol. In the srsRAN Project implementation of the CU-CP, there is five main components and 
four main interfaces. The CU-CP communicates directly with the 5G Core (via the N2 interface), the CU-UP (via the E1 interface), the DU-high (via the F1-c interface) and can also be connected to the near-RT RIC (via the E2 interface). This implementation
takes a UE-centric approach. 



**Components:**

    - :ref:`CU-UP Processor <cu_up_processor>`: Custom component for handling each CU-UP connected to the CU-CP. Multiple CU-UPs can be connected to one CU-CP, as a result the E1AP is created inside the CU-UP processor for each connected CU-UP.
    - :ref:`DU Processor <du_processor>`: Custom component for handling DUs for connected to the CU-CP. Each connected DU has its own DU processor with bundled F1AP, PDCP, and RRC procedures. Each UE connected to the DU also has its own RRC UE containing the PDCP processes. 
    - :ref:`UE Manager <ue_manager>`: Custom component for managing connected UEs in the CU-CP. Responsible for adding and removing UEs and providing relevant UE information to other processes. Communicates information to/from the CU-UP, DU and Core.
    - :ref:`Measurement Manager <measurement_manager>`: Custom component for managing cell measurement within the gNB. 
    - :ref:`Mobility Manager <mobility_manager>`: Custom component for managing UE mobility in the CU-CP. 

**Interfaces:**

    - :ref:`E2 <E2_cp>`: Interface with the near-RT RIC.
    - :ref:`E1 <E1AP_cu_cp>`: Interface with the CU-UP.
    - :ref:`F1-c <F1AP_cu>`: Control plane interface with the DU.
    - :ref:`N2 <NGAP_cu>`: Control plane interface with the 5G Core (AMF).
     

-----

 .. toctree::
    :maxdepth: 1
    :caption: CU-CP Contents

    cu_up_processor.rst
    du_processor.rst
    ue_manager.rst
    measurement_manager.rst
    mobility_manager.rst
    E2AP_cu_cp.rst
    NGAP_cu.rst
    
    
