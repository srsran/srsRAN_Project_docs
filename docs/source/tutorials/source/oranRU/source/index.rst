.. _oran_ru_tutorial: 

srsRAN gNB with ORAN RU
#######################

Overview
********

srsRAN Project supports :ref:`O-RAN Split 7.2 <7_2_split>` and Split 8. Split 7.2 supports the uncoupling of radio hardware and baseband processing through the Fronthaul interface. In this turorial 
we will demonstrate how to connect the srsRAN Project gNB to an O-RAN RU using Split 7.2. For this example we will demonstrate the `Benetel RAN550 RU <https://benetel.com/ran550/>`_. Benetel are one of Software Radio Systems' RU partners.  

Split 7.2 is supported through the Open Fronthaul Library (OFH Lib), which is a new library written by the team at Software Radio Systems to enable easy integration with RUs over the Fronthaul interface. OFH Lib is a fully open-source library that 
has been designed and completely implemented by SRS with zero dependencies on 3rd party software. It has been designed to minimize the integration and configuration burden associated with integrating O-RAN CU/DU solutions with 3rd-party RUs. 

----

Setup Considerations
********************

.. image:: .imgs/benetel_setup_detailed.png
    :width: 60%
    :align: center

For this tutorial the following hardware and software is used: 

    - Custom Server (Running srsRAN Project CU/DU)

      - CPU: AMD Ryzen 7 5700G with Radeon Graphics
      - MEM: 64GB
      - NIC: Intel Corporation 82599ES 10-Gigabit
      - OS: Ubuntu 22.04 (currently 5.15.0-1037-realtime)

    - `srsRAN Project <https://github.com/srsran/srsRAN_project>`_  (23.05 or later)
    - `Benetel RAN550 RU <https://benetel.com/ran550/>`_
    - `Falcon-RX/812/G xHaul Switch (w/ PTP Grandmaster) <https://www.fibrolan.com/Falcon-RX>`_
    - `Open5GS 5G Core <https://open5gs.org/>`_
    - `Amarisoft UE <https://www.amarisoft.com/technology/ue-simulator/>`_  (2021-09-18 or later)

DU 
=====

The DU is provided by the srsRAN Project gNB. As mentioned the Open Fonthaul Library (OFH Lib) provides the necessary interface between the DU and the RU. The DU is connected to the RU via cable. 

RU 
=====

The Benetel RAN550 RU is used as the RU in this setup. This is a Split 7.2x indoor O-RU. 

5G Core
=======

For this example we are using Open5GS as the 5G Core.

Open5GS is a C-language Open Source implementation for 5G Core and EPC. The following links will provide you
with the information needed to download and setup Open5GS so that it is ready to use with srsRAN 4G:

    - `GitHub <https://github.com/open5gs/open5gs>`_
    - `Quickstart Guide <https://open5gs.org/open5gs/docs/guide/01-quickstart/>`_

Switch
======

The Falcon-RX switch is a 5G xHaul Timing Aware O-RAN Switch & PTP Grandmaster. This is used to sync both the DU and RU. 

Clocking & Synchronization
--------------------------

O-RAN WG 4 has defined various synchronization methods for use with Open Fronthaul. These are outlined in O-RAN.WG4.CUS.0-R003-v11.00 Section 11. The latest version of the specifications can be downloaded `here <https://orandownloadsweb.azurewebsites.net/specifications>`_.

In this setup we use LLS-C2, this is defined as the following: 

    *Configuration LLS-C2: with this topology, the O-DU is part of the synchronization chain towards the O-RU.
    Network timing is distributed from O-DU to O-RU between O-DU sites and O-RU sites. One or more Ethernet
    switches are allowed in the fronthaul network. Interconnection among switches and fabric topology (for
    example mesh, ring, tree, spur etc.) are deployment decisions which are out of the scope of the present
    document.*

In the ths described setup the Falcon xHaul Switch is providing the PTP Grandmaster (which is synchronized via GPS) to the RU and the DU. These are connected to the SFP 10G ports on the switch via ethernet. 

----

Configuration
*************

Falcon-RX
=========

SyncCenter
-----------

The switch must be connected to a GPS antenna to ensure the PTP Grandmaster is synchronized correctly. Once connected it is important to check that the GPS has been locked correctly and an accurate clock source is being provided.

.. image:: .imgs/sync_center.png
    :align: center  

To do this, navigate to the FalconRX configuration GUI and go to *Configuration > Timing > SyncCenter* and select ``GPS`` as the ``Sync Source Type``. Once this is done, wait for the GPS to lock and synchronize correctly. The SyncCenter will
display as green once it has successfully locked to the GPS signal. This is shown in the above image.

PTP Clocks
----------

Once the PTP Grandmaster is successfully synchronized it must be configured correctly for use with the DU and RU. 

.. image:: .imgs/ptp_config_1.png
   :align: center

First, go to *Configuration > Timing > PTP* and add a new PTP Clock. Select ``Device Type: Master Only`` and ``Profile: G8275.1``. This is shown in the above image. After adding the PTP clock, click on the Clock Instance that you want to edit.

.. image:: .imgs/ptp_config_2.png
   :align: center

Once you have selected the Clock Instance you want to edit, set the ``VLAN ID`` to ``1588`` and activate all ports that you want to serve with PTP. From now on the PTP is sent with VLAN ID 1588. 

You should now save your configuration. 

VLAN
-----

Next, the VLANs must be configured correctly so as to allow the DU and RU to receive the PTP sync from the Grandmaster. 

.. image:: .imgs/ptp_vlan.png
   :align: center

Go to *Configuration > VLANs > Configuration* to correctly configure the VLAN settings. First, set ``Allowed Access VLANs:`` as  ``1,2``. Next, configure the ports you want to use as ``Trunk`` ports, set the ``Port VLAN`` as  ``1588``, and 
set ``Egress Tagging`` as ``Untag Port VLAN``. In the ``Allowed VLANs`` field you can set a range or specify specific VLANs. For example, here we are specifying ``1,2,1588``. You **must** include ``1588`` otherwise the DU and RU will not correctly 
receive the PTP sync. 

gNB
=====


RU 
=====

----

Connecting the RU
*****************

COTS UE
=======

AmariUE 
========

----

Troubleshooting
***************

----

Tested Devices
**************
