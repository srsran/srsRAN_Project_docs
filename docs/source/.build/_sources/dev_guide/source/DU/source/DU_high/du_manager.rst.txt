
.. _DU_manager: 

DU Manager
**********

Overview
========

The DU manager acts as a mediator in the process of configuring different layers of the DU. It is particularly important in the pre-operational 
stage, when it provides  system information to the FAPI, MAC and F1AP that is essential to their operation. The DU manager is also essential 
during the operational stage, in the creation/reconfiguration/deletion of UEs and in the dynamic connection between bearers across different layers.

The main responsibilities of the DU Manager include:

    - Configuring the MAC, FAPI and F1AP during the pre-operational stage with relevant DU system information, such as supported DU cells and their configuration
    - Orchestration of the creation/reconfiguration/removal of UEs in the DU, in particular, the setting up of UE contexts in the MAC, FAPI and F1AP.
    - Orchestration of the creation/reconfiguration/removal of UE bearers in MAC, RLC and F1AP, and connection of each bearer with its respective upper and lower layers.
    - Management of commands received through E2.