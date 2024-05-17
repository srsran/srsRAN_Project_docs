.. _liteon:

LiteOn FlexFi
#############

Overview 
********
This guide provides further details on connecting the srsRAN CU/DU to an RU using the the ORAN 7.2 split. Specifically, the `LiteOn FlexFi <https://www.liteon.com/en-us/product/714>`_.  



-----

Configuration
*************

CU/DU
=====

You can download a sample gNB configuration file that is compatible with the LiteOn FlexFI RU :download:`here <.configs/gnb_ru_liteon_tdd_n78_100mhz.yml>`.

This configuration file will allow you to create a 100MHz SISO TDD cell in band n78. 

RU
==

First, power on and access the RU via the command line. The RU must then be configured and power-cycled before it can be used. 

The following commands are used to configure the RU, they are shown with the command first and then the associated output: 

.. code-block:: bash 

    (config)# compression-bit 9
    Old Compression Bit = 8
    New Compression Bit = 9
    
    (config)# du-mac-address
    DU MAC Address = 001122334466
    
    (config)# du-mac-address 80615f0ddfab
    Old DU MAC Address = 001122334466
    New DU MAC Address = 80615f0ddfab
    
    (config)# jumboframe 1
    Old jumboframe = 0x00000000
    New jumboframe = 0x00000001
    
    (config)# phasecomp-mode true
    phase compensation mode : Enable
    
    (config)# slot-id
    slotid = 0x00000002
    
    (config)# slot-id 1
    Old slotid = 0x00000002
    New slotid = 0x00000001
    
    (config)# sync-source PTP
    sync source : PTP
    Active after reboot

The RU should now be power-cycled. Once completed successfully, the RU is ready to be used. 

------

Initializing and connecting to the network
******************************************

You can now initialize the network and connect to it as normal. 

.. note:: 

    A more detailed version of this guide is currently in development. For help with issues and troubleshooting please go to the GitHub Discussions. 