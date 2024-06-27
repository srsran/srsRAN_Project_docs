.. _liteon:

LITEON FlexFi
#############

Overview 
********
This guide provides further details on connecting the srsRAN CU/DU to an RU using the the ORAN 7.2 split. Specifically, the `LITEON FlexFi <https://www.liteon.com/en-us/product/714>`_.
We've tested with a model FF-RFI078I4 with firmware version 02.00.09.


-----

Configuration
*************

CU/DU
=====

You can download a sample gNB configuration file that is compatible with the LITEON FlexFI RU :download:`here <.configs/gnb_ru_liteon_tdd_n78_100mhz.yml>`.

This configuration file will allow you to create a 100MHz TDD 2T1R cell in band n78. 

RU
==

The RU needs to be flashed with firmware >= 02.00.09. Older firmware versions will not work correctly.

First, power on and access the RU via the command line. The RU must then be configured and power-cycled before it can be used. 

The following commands are used to configure the RU, they are shown with the command first and then the associated output: 

.. code-block:: bash 

    (config)# compression-bit 9
    Old Compression Bit = 8
    New Compression Bit = 9
    
    (config)# du-mac-address 80615f0ddfab
    Old DU MAC Address = 001122334466
    New DU MAC Address = 80615f0ddfab
    
    (config)# jumboframe 1
    Old jumboframe = 0x00000000
    New jumboframe = 0x00000001
    
    (config)# phasecomp-mode true
    phase compensation mode : Enable
    
    (config)# slot-id 1
    Old slotid = 0x00000002
    New slotid = 0x00000001
    
    (config)# sync-source PTP
    sync source : PTP
    Active after reboot
    
    (config)# tick 1
    Old tick = 0x00000001
    New tick = 0x00000001
    
    (config)# c/u-plane-vlan
    control and user Plane vlan = 564

    (config)# center-frequency
    Center Frequency = 3749700000


The RU should now be power-cycled. Once completed successfully, the RU state can be checked with:

.. code-block:: bash 

    # show oru-status
    Sync State  : SYNCHRONIZED
    RF State    : Ready
    DPD         : Ready
    DuConnected : notReady

Note that at this stage the DU is not generating any traffic.

------

Initializing the network
========================

The following steps should be taken to initialize the network: 

1. Ensure the RU is started and has PTP lock (see above).

2. Run the CU/DU, making sure that the PTP sync between the DU and the Falcon switch is successful as previously outlined.  

   .. code-block:: bash

     sudo ./gnb -c gnb_ru_liteon_tdd_n78_100mhz.yml

   If the DU connects to the RU successfully, you will see the following output: 

   .. code-block:: bash

        The PRACH detector will not meet the performance requirements with the configuration {Format B4, ZCZ 0, SCS 30kHz, Rx ports 1}.

        --== srsRAN gNB (commit 61bce3657a) ==--

        Connecting to AMF on 10.12.1.105:38412
        Initializing the Open Fronthaul Interface for sector#0: ul_compr=[BFP,9], dl_compr=[BFP,9], prach_compr=[BFP,9], prach_cp_enabled=true, downlink_broadcast=false
        Cell pci=1, bw=100 MHz, 2T1R, dl_arfcn=649980 (n78), dl_freq=3749.7 MHz, dl_ssb_arfcn=647232, ul_freq=3749.7 MHz

        ==== gNodeB started ===
        Type <t> to view trace


3. If you have the DU running you can go back to the SSH console on the RU and check that the fronthaul traffic is arriving on time. For this run: 

   .. code-block:: bash 

        # show oru-status
        Sync State  : SYNCHRONIZED
        RF State    : Ready
        DPD         : Ready
        DuConnected : Ready

  ``DuConnected`` is now Ready indicating that the RU is receiving traffic and radiating. The RU performance metrics can be checked with:

  .. code-block:: bash
    
    # show pm-data
    1,POWER,2024-06-26T17:09:53Z,2024-06-26T17:10:10Z,o-ran-hardware:O-RU-FPGA,8.6181,9.5173,8.8625,iana-hardware:cpu,8.6181,9.5173,8.8625
    2,TEMPERATURE,2024-06-26T17:09:53Z,2024-06-26T17:10:10Z,o-ran-hardware:O-RU-FPGA,62.0732,64.5135,63.5156,iana-hardware:cpu,62.5706,64.9642,63.4276
    13,VOLTAGE,2024-06-26T17:09:53Z,2024-06-26T17:10:27Z,0,0.0000,2024-06-26T17:09:54Z,1.8311,2024-06-26T17:09:55Z,0.0000,2024-06-26T17:09:54Z,0.0000,2024-06-26T17:10:27Z,3749700000
    1,POWER,2024-06-26T17:10:10Z,2024-06-26T17:10:27Z,o-ran-hardware:O-RU-FPGA,8.6181,9.6016,9.0758,iana-hardware:cpu,8.6181,9.6016,9.0758
    2,TEMPERATURE,2024-06-26T17:10:10Z,2024-06-26T17:10:27Z,o-ran-hardware:O-RU-FPGA,62.5085,64.7777,63.5053,iana-hardware:cpu,62.0111,64.9021,63.2120
    1,RX_ON_TIME,2024-06-26T17:09:53Z,2024-06-26T17:10:27Z,ru1,6863018
    2,RX_EARLY,2024-06-26T17:09:53Z,2024-06-26T17:10:27Z,ru1,0
    3,RX_LATE,2024-06-26T17:09:53Z,2024-06-26T17:10:27Z,ru1,0
    6,RX_TOTAL,2024-06-26T17:09:53Z,2024-06-26T17:10:27Z,ru1,7354134
    7,RX_ON_TIME_C,2024-06-26T17:09:53Z,2024-06-26T17:10:27Z,ru1,490546
    8,RX_EARLY_C,2024-06-26T17:09:53Z,2024-06-26T17:10:27Z,ru1,0
    9,RX_LATE_C,2024-06-26T17:09:53Z,2024-06-26T17:10:27Z,ru1,0
    1,TX_TOTAL,2024-06-26T17:09:53Z,2024-06-26T17:10:27Z,ru1,3976


  Verify that the the values in the ``RX_ON_TIME``, ``RX_ON_TIME_C`` and ``TX_TOTAL`` column increase but all other columns should be zero.

Connecting to the network
=========================

You can now connect a UE to the network. This can be done using e.g. a COTS UE. See the main RU guide for details on this.