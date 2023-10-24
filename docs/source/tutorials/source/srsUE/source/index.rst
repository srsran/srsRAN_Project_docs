.. srsRAN gNB with srsUE

.. _srsue_appnote:

srsRAN gNB with srsUE
#####################

Introduction
************

srsRAN Project is a 5G CU/DU solution and does not include a UE application. However, `srsRAN 4G <https://github.com/srsran/srsRAN_4G>`_ does include a prototype 5G UE (srsUE) which can be used for testing.
This application note shows how to create an end-to-end fully open-source 5G network with srsUE, the srsRAN Project gNodeB and Open5GS 5G core network. 

First, we show how to connect srsUE to the gNodeB over-the-air using USRPs. In the second part, we outline how to use virtual radios based on ZeroMQ instead of SDR hardware.
Virtual radios allow the UE to be connected to the gNodeB over sockets. This approach can be very useful for development, testing, debugging, CI/CD or for teaching and demonstrating.

----- 

Hardware and Software Overview
******************************

For this application note, the following hardware and software are used:

    - PC with Ubuntu 22.04.1
    - `srsRAN Project <https://github.com/srsran/srsRAN_project>`_
    - `srsRAN 4G <https://github.com/srsran/srsRAN_4G>`_ (23.04 or later)
    - `Two Ettus Research USRP B210s <https://www.ettus.com/all-products/ub210-kit/>`_ (connected over USB3)
    - `Open5GS 5G Core <https://open5gs.org/>`_
    - `ZeroMQ <https://zeromq.org/>`_

Ideally the USRPs would be connected to a 10 MHz external reference clock or GPSDO, although this is not a strict requirment. We recommend the `Leo Bodnar GPSDO <http://www.leobodnar.com/shop/index.php?main_page=product_info&cPath=107&products_id=234&zenid=5194baec39dbc91212ec4ac755a142b6>`_.

srsRAN 4G
=========

If you have not already done so, install the latest version of srsRAN 4G and all of its dependencies. This is outlined in the `installation guide <https://docs.srsran.com/projects/4g/en/latest/general/source/1_installation.html>`_. 

Please check our srsRAN 4G `ZeroMQ Application Note <https://docs.srsran.com/projects/4g/en/latest/app_notes/source/zeromq/source/index.html>`_ for information on installing ZMQ and using it with srsRAN 4G.


Limitations
-----------

The current srsUE implementation has a few feature limitations when running in 5G SA mode. The key feature limitations are as follows:

  - Limited to 15 kHz Sub-Carrier Spacing (SCS), which means only FDD bands can be used. 
  - Limited to 10 MHz Bandwidth (BW)

Open5GS
=======

For this example we are using Open5GS as the 5G Core. 

Open5GS is a C-language Open Source implementation for 5G Core and EPC. The following links will provide you 
with the information needed to download and set-up Open5GS so that it is ready to use with srsRAN: 

    - `GitHub <https://github.com/open5gs/open5gs>`_ 
    - `Quickstart Guide <https://open5gs.org/open5gs/docs/guide/01-quickstart/>`_

ZeroMQ
======

On Ubuntu, ZeroMQ development libraries can be installed with:

.. code::

  sudo apt-get install libzmq3-dev
  
Alternatively, ZeroMQ can also be built from source. 

First, one needs to install libzmq:

.. code::

  git clone https://github.com/zeromq/libzmq.git
  cd libzmq
  ./autogen.sh
  ./configure
  make
  sudo make install
  sudo ldconfig

Second, install czmq:

.. code::

  git clone https://github.com/zeromq/czmq.git
  cd czmq
  ./autogen.sh
  ./configure
  make
  sudo make install
  sudo ldconfig

Finally, you need to compile srsRAN Project and srsRAN 4G (assuming you have already installed all the required dependencies). 
Note, if you have already built and installed srsRAN 4G and srsRAN Project prior to installing ZMQ and other dependencies you 
will have to re-build both to ensure the ZMQ drivers have been recognized correctly. 

For srsRAN Project, the following commands can be used to download and build from source: 

.. code::

  git clone https://github.com/srsran/srsRAN_Project.git
  cd srsRAN_Project
  mkdir build
  cd build
  cmake ../ -DENABLE_EXPORT=ON -DENABLE_ZEROMQ=ON
  make -j`nproc`

ZeroMQ is disbaled by default, this is enabled when running ``cmake`` by including ``-DENABLE_EXPORT=ON -DENABLE_ZEROMQ=ON``. 

Pay extra attention to the cmake console output. Make sure you read the following line:

.. code::

  ...
  -- FINDING ZEROMQ.
  -- Checking for module 'ZeroMQ'
  --   No package 'ZeroMQ' found
  -- Found libZEROMQ: /usr/local/include, /usr/local/lib/libzmq.so
  ...

----- 

Over-the-air Setup
******************

The following diagram presents the setup architecture:

.. figure:: .imgs/gNB_srsUE_usrp.png
  :align: center


Configuration
=============

You can find the srsRAN Project gNB configuration file for this example in the ``configs`` folder of the srsRAN Project source files. You can also find it `here <https://github.com/srsran/srsRAN_Project/tree/main/configs>`_: 

 
  * `gNB FDD srsUE config <https://github.com/srsran/srsRAN_Project/blob/main/configs/gnb_rf_b210_fdd_srsUE.yml>`_

You can download the srsUE config here: 

  * :download:`srsUE <.config/ue_rf.conf>`

It is recommended you use these files to avoid errors while changing configs manually. Any configuration files not included here do not require modification from the default settings.
Details of the modifications made are outlined in following sections.


Open5GS Core
------------

As highlighted above, the Open5GS `5G Core Quickstart Guide <https://open5gs.org/open5gs/docs/guide/01-quickstart/#:~:text=restart%20open5gs%2Dsgwud-,Setup%20a%205G%20Core,-You%20will%20need>`_ provides a comprehensive overview of how to configure Open5GS to run as a 5G Core. 

The main modifications needed are: 

    - Change the TAC in the AMF config to 7
    - Check that the NGAP, and GTPU addresses are all correct. This is done in the AMF and UPF config files.
    - Make sure the PLMN values are consistent across all config files (i.e., Open5GS, gNB, srsUE config files). We use PLMN: "00101".

The final step is to register the UE to the list of subscribers through the Open5GS WebUI. The values for each field should match the values associated with the USIM being used. In this case these are defined in the UE config file, these values should be used to populate the relevant fields when registering the USIM with the core. 

.. note::
   Make sure to correctly configure the APN (here we use *srsapn*), if this is not done correctly the UE will not connect correctly.

gNB
---
The following changes need to be made to the gNB configuration file.

The gNB has to connect to AMF in the 5G core network, therefore we need to provide two IP addresses::

  amf:
    addr: 10.53.1.2                  # The address of the AMF. Check Open5GS config -> amf -> ngap -> addr
    bind_addr: 10.53.1.1             # A local IP that the gNB binds to for traffic from the AMF.

Next, we have to configure the RF front-end device::

  ru_sdr:
    device_driver: uhd                # The RF driver name.
    device_args: type=b200            # Optionally pass arguments to the selected RF driver.
    clock: external                   # Specify the clock source used by the RF.
    sync: external                    # Specify the sync source used by the RF.
    srate: 11.52                      # RF sample rate might need to be adjusted according to selected bandwidth.
    tx_gain: 75                       # Transmit gain of the RF might need to adjusted to the given situation.
    rx_gain: 75                       # Receive gain of the RF might need to adjusted to the given situation.

Finally, we configure the 5G cell parameters::

  cell_cfg:
    dl_arfcn: 368500                  # ARFCN of the downlink carrier (center frequency).
    band: 3                           # The NR band.
    channel_bandwidth_MHz: 10         # Bandwith in MHz. Number of PRBs will be automatically derived.
    common_scs: 15                    # Subcarrier spacing in kHz used for data.
    plmn: "00101"                     # PLMN broadcasted by the gNB.
    tac: 7                            # Tracking area code (needs to match the core configuration).
    pdcch:
      dedicated:
        ss2_type: common              # Search Space type, has to be set to common
        dci_format_0_1_and_1_1: false # Set correct DCI format (fallback)
    prach:
      prach_config_index: 1

srsUE
-----

The following changes need to be made to the UE configuration file to allow it to connect to the gNB in SA mode. 

First, the following parameters need to be changed under the **[rf]** options so that the B210 is configured optimally:: 

  [rf]
  freq_offset = 0
  tx_gain = 50
  rx_gain = 40
  srate = 11.52e6
  nof_antennas = 1

  device_name = uhd
  device_args = clock=external
  time_adv_nsamples = 300

The next set of changes need to be made to the **[rat.eutra]** options. The LTE carrier is disabled, to force the UE to use a 5G NR carrier:: 

  [rat.eutra]
  dl_earfcn = 2850
  nof_carriers = 0

Then, the **[rat.nr]** options need to be configured for 5G SA mode operation:: 

  [rat.nr]
  bands = 3
  nof_carriers = 1

Lastly, set the release and ue_category:: 

  [rrc]
  release = 15
  ue_category = 4

Note that the following (default) USIM Credentials are used:: 

  [usim]
  mode = soft
  algo = milenage
  opc  = 63BFA50EE6523365FF14C1F45F88737D
  k    = 00112233445566778899aabbccddeeff
  imsi = 001010123456780
  imei = 353490069873319

The APN is enabled with the following configuration:: 

  [nas]
  apn = srsapn
  apn_protocol = ipv4 


Running the Network
===================

The following order should be used when running the network: 

	1. 5GC
	2. gNB
	3. UE

Open5GS Core
------------

Once the Open5GS core has been configured following the steps described above, it is important to restart the relevant daemons (especially, AMF and UPF) so that any config changes made can take effect.
Note that the core is a service running in the background, so there is no need to start directly. 

	
gNB
---

We run gNB directly from the build folder (the config file is also located there) with the following command::
	
	sudo ./gnb -c ./gnb.yaml
	
The console output should be similar to:: 

  --== srsRAN gNB (commit c037a65c8) ==--

  Connecting to AMF on 10.53.1.2:38412
  [INFO] [UHD] linux; GNU C++ version 9.2.1 20200304; Boost_107100; UHD_3.15.0.0-2build5
  [INFO] [LOGGING] Fastpath logging disabled at runtime.
  Making USRP object with args 'type=b200'
  [INFO] [B200] Detected Device: B210
  [INFO] [B200] Operating over USB 3.
  [INFO] [B200] Initialize CODEC control...
  [INFO] [B200] Initialize Radio control...
  [INFO] [B200] Performing register loopback test... 
  [INFO] [B200] Register loopback test passed
  [INFO] [B200] Performing register loopback test... 
  [INFO] [B200] Register loopback test passed
  [INFO] [B200] Setting master clock rate selection to 'automatic'.
  [INFO] [B200] Asking for clock rate 16.000000 MHz... 
  [INFO] [B200] Actually got clock rate 16.000000 MHz.
  [INFO] [MULTI_USRP] Setting master clock rate selection to 'manual'.
  [INFO] [B200] Asking for clock rate 11.520000 MHz... 
  [INFO] [B200] Actually got clock rate 11.520000 MHz.
  Cell pci=1, bw=10 MHz, dl_arfcn=368500 (n3), dl_freq=1842.5 MHz, dl_ssb_arfcn=368410, ul_freq=1747.5 MHz

The ``Connecting to AMF on 10.53.1.2:38412`` message indicates that gNB initiated a connection to the core. 
If the connection attempt is successful, the following (or similar) will be displayed on the Open5GS console::

  Open5GS    | 04/17 10:00:43.567: [amf] INFO: gNB-N2 accepted[10.53.1.1]:41578 in ng-path module (../src/amf/ngap-sctp.c:113)
  Open5GS    | 04/17 10:00:43.567: [amf] INFO: gNB-N2 accepted[10.53.1.1] in master_sm module (../src/amf/amf-sm.c:706)
  Open5GS    | 04/17 10:00:43.567: [amf] INFO: [Added] Number of gNBs is now 1 (../src/amf/context.c:1034)
  Open5GS    | 04/17 10:00:43.567: [amf] INFO: gNB-N2[10.53.1.1] max_num_of_ostreams : 30 (../src/amf/amf-sm.c:745)

srsUE
-----

Finally, we start srsUE. This is also done directly from within the build folder, with the config file in the same location::

	sudo ./srsue ue.conf

If srsUE connects successfully to the network, the following (or similar) should be displayed on the console:: 
  
  Reading configuration file ./ue.conf...

  Built in Release mode using commit 637e7ce9f on branch dev.

  Opening 1 channels in RF device=default with args=clock=external
  Supported RF device list: UHD zmq file
  Trying to open RF device 'UHD'
  [INFO] [UHD] linux; GNU C++ version 9.2.1 20200304; Boost_107100; UHD_3.15.0.0-2build5
  [INFO] [LOGGING] Fastpath logging disabled at runtime.
  [INFO] [MPMD FIND] Found MPM devices, but none are reachable for a UHD session. Specify find_all to find all devices.
  Opening USRP channels=1, args: type=b200,master_clock_rate=23.04e6
  [INFO] [UHD RF] RF UHD Generic instance constructed
  [INFO] [B200] Detected Device: B210
  [INFO] [B200] Operating over USB 3.
  [INFO] [B200] Initialize CODEC control...
  [INFO] [B200] Initialize Radio control...
  [INFO] [B200] Performing register loopback test... 
  [INFO] [B200] Register loopback test passed
  [INFO] [B200] Performing register loopback test... 
  [INFO] [B200] Register loopback test passed
  [INFO] [B200] Asking for clock rate 23.040000 MHz... 
  [INFO] [B200] Actually got clock rate 23.040000 MHz.
  RF device 'UHD' successfully opened
  Setting manual TX/RX offset to 300 samples
  Waiting PHY to initialize ... done!
  Attaching UE...
  Random Access Transmission: prach_occasion=0, preamble_index=0, ra-rnti=0x39, tti=2094
  Random Access Complete.     c-rnti=0x4602, ta=0
  RRC Connected
  PDU Session Establishment successful. IP: 10.45.10.2
  RRC NR reconfiguration successful.


It is clear that the connection has been made successfully once the UE has been assigned an IP, this is seen in ``PDU Session Establishment successful. IP: 10.45.10.2``. 
The NR connection is then confirmed with the ``RRC NR reconfiguration successful.`` message. 

Testing the Network
===================

Here, we demonstrate how to use ping and iPerf3 tools to test the connectivity and throughput in the network.

Ping
----

Ping is the simplest tool to test the end-to-end connectivity in the network, i.e., it tests whether the UE and core can communicate. 


* **Uplink**
To test the connection in the uplink direction, run the following command from the UE machine:: 

    ping 10.45.10.1

* **Downlink**
To test the connection in the downlink direction, run the following command from the gNB machine:: 

    ping 10.45.10.2

The IP for the UE can be taken from the UE console output. This might change each time a UE reconnects to the network, so it is best practice to always double-check the latest IP assigned by reading it 
from the console before running the downlink traffic.


* **Ping Output**

Example **ping** output:: 

  # ping 10.45.10.1 -c 4
  PING 10.45.10.1 (10.45.10.1) 56(84) bytes of data.
  64 bytes from 10.45.10.1: icmp_seq=1 ttl=64 time=39.9 ms
  64 bytes from 10.45.10.1: icmp_seq=2 ttl=64 time=38.9 ms
  64 bytes from 10.45.10.1: icmp_seq=3 ttl=64 time=37.0 ms
  64 bytes from 10.45.10.1: icmp_seq=4 ttl=64 time=36.1 ms

  --- 10.45.10.1 ping statistics ---
  4 packets transmitted, 4 received, 0% packet loss, time 3004ms
  rtt min/avg/max/mdev = 36.085/37.952/39.859/1.493 ms


iPerf3 
------

iPerf3 is a tool that generates (TCP and UDP) traffic and measures parameters (e.g., throughput and packet loss) of the traffic flow.

In this example, we generate traffic in the uplink direction. To this end, we run an iPerf3 client on the UE side and a server on the network side. UDP traffic will be generated at 10Mbps for 60 seconds. It is important to start the server first, and then the client.

* **Network-side**

Start the iPerf3 server:: 

  iperf3 -s -i 1 

The server listens for traffic coming from the UE. After the client connects, the server prints flow measurements every second.

* **UE-side**

With the network and the iPerf3 server up and running, the client can be run from the UE's machine with the following command:: 

  iperf3 -c 10.45.10.1 -b 10M -i 1 -t 60 

Traffic will now be sent from the UE to the network. This will be shown in both the server and client consoles. Additionaly, we will observe console traces of the UE and the gNB. 


* **Iperf3 Output**

Example **server** iPerf3 output:: 

  # iperf3 -s -i 1 
  -----------------------------------------------------------
  Server listening on 5201
  -----------------------------------------------------------
  Accepted connection from 10.45.10.2, port 40544
  [  5] local 10.45.10.1 port 5201 connected to 10.45.10.2 port 40546
  [ ID] Interval           Transfer     Bitrate
  [  5]   0.00-1.00   sec  1.20 MBytes  10.1 Mbits/sec                  
  [  5]   1.00-2.00   sec  1.22 MBytes  10.2 Mbits/sec                  
  [  5]   2.00-3.00   sec  1.16 MBytes  9.71 Mbits/sec                  
  [  5]   3.00-4.00   sec  1.12 MBytes  9.44 Mbits/sec                  
  [  5]   4.00-5.00   sec  1.25 MBytes  10.5 Mbits/sec                  
  [  5]   5.00-6.00   sec  1.25 MBytes  10.5 Mbits/sec                  

Example **client** iPerf3 output:: 

  # iperf3 -c 10.45.10.1 -b 10M -i 1 -t 60 
  Connecting to host 10.45.10.1, port 5201
  [  5] local 10.45.10.2 port 40546 connected to 10.45.10.1 port 5201
  [ ID] Interval           Transfer     Bitrate         Retr  Cwnd
  [  5]   0.00-1.00   sec  1.20 MBytes  10.1 Mbits/sec    0    117 KBytes       
  [  5]   1.00-2.00   sec  1.25 MBytes  10.5 Mbits/sec    0    130 KBytes       
  [  5]   2.00-3.00   sec  1.25 MBytes  10.5 Mbits/sec    0    130 KBytes       
  [  5]   3.00-4.00   sec  1.12 MBytes  9.44 Mbits/sec    0    130 KBytes       
  [  5]   4.00-5.00   sec  1.25 MBytes  10.5 Mbits/sec    0    130 KBytes       
  [  5]   5.00-6.00   sec  1.12 MBytes  9.44 Mbits/sec    0    130 KBytes 

* **Console Traces**

The following example trace was taken from the **srsUE console** while running the above iPerf3 test:: 

  ---------Signal-----------|-----------------DL-----------------|-----------UL-----------
  rat  pci  rsrp   pl   cfo | mcs  snr  iter  brate  bler  ta_us | mcs   buff  brate  bler
   nr    1     0    0 -457m |  27   43   1.3   274k    0%    0.0 |  27   136k    13M    0%
   nr    1     0    0 -122m |  27   43   1.4   285k    0%    0.0 |  27    0.0    13M    0%
   nr    1     0    0 -282m |  27   43   1.3   267k    0%    0.0 |  27    47k    13M    0%
   nr    1     0    0  -14m |  27   43   1.4   274k    0%    0.0 |  27    3.0    13M    0%
   nr    1     0    0 -373m |  27   43   1.4   268k    0%    0.0 |  27    47k    13M    0%
   nr    1     0    0  244m |  27   43   1.3   274k    0%    0.0 |  27    0.0    13M    0%


To read more about the UE console trace metrics, see the `UE User Manual <https://docs.srsran.com/projects/4g/en/latest/usermanuals/source/srsue/source/6_ue_commandref.html#ue-commandref>`_.

The following example trace was taken from the **gNB console** at the same time period as the srsUE trace shown above:: 

           -------------DL----------------|------------------UL--------------------
 pci rnti  cqi  mcs  brate   ok  nok  (%) | pusch  mcs  brate   ok  nok  (%)    bsr
   1 4601   15   27   275k  328    0   0% |  23.2   28    13M  398    0   0%  55.5k
   1 4601   15   27   266k  336    0   0% |  23.1   28    13M  387    0   0%    0.0
   1 4601   15   27   284k  349    0   0% |  23.1   28    13M  410    1   0%    0.0
   1 4601   15   27   258k  315    0   0% |  23.1   28    12M  371    0   0%    0.0
   1 4601   15   27   275k  330    0   0% |  23.2   28    13M  394    0   0%  55.5k
   1 4601   15   27   265k  332    0   0% |  23.2   28    13M  386    1   0%    0.0


-----

ZeroMQ-based Setup
******************

In this section, we describe the steps required to configure the ZMQ-based RF driver in both gNB and srsUE.
The following diagram presents the setup architecture:

.. figure:: .imgs/gNB_srsUE_zmq.png
  :align: center

Configuration
=============

The following config files were modified to use ZMQ-based RF driver:

  * :download:`gNB config <.config/gnb_zmq.yaml>`
  * :download:`UE config <.config/ue_zmq.conf>`

Details of the modifications made are outlined in following sections.

gNB
---
Replacing the UHD driver with the ZMQ-based RF driver requires changing only **ru_sdr** sections of the gNB file::

  ru_sdr:
    device_driver: zmq
    device_args: tx_port=tcp://127.0.0.1:2000,rx_port=tcp://127.0.0.1:2001,base_srate=11.52e6
    srate: 11.52
    tx_gain: 75
    rx_gain: 75


srsUE
-----
When using the ZMQ-based RF driver in the srsUE, it is important to create an appropriate network namespace in the host machine. 
This is achieved with the following command::

    sudo ip netns add ue1

To verify the new "ue1" network namespace exists, run::   

    sudo ip netns list

Then, the **[rf]** section in the srsUE config file has to be changed as follows:: 

  [rf]
  freq_offset = 0
  tx_gain = 50
  rx_gain = 40
  srate = 11.52e6
  nof_antennas = 1

  device_name = zmq
  device_args = tx_port=tcp://127.0.0.1:2001,rx_port=tcp://127.0.0.1:2000,base_srate=11.52e6


In addition, the srsUE must be configured to use the created network namespace. This is achieved by updating the **[gw]** section of the config file:: 

  [gw]
  netns = ue1
  ip_devname = tun_srsue
  ip_netmask = 255.255.255.0


Running the Network
===================

Once the config files are updated, the network can be set up on a single host machine, using the same commands as in the case of the over-the-air setup.


Testing the Network
===================

Ping
----

* **Uplink**
To test the connection in the uplink direction, use the following:: 

    sudo ip netns exec ue1 ping 10.45.1.1

* **Downlink**
To run ping in the downlink direction, use:: 

    ping 10.45.1.2

The IP for the UE can be taken from the UE console output. This might change each time a UE reconnects to the network, so it is best practice to always double-check the latest IP assigned by reading it from the console before running the downlink traffic.

* **Ping Output**

Example **ping** output:: 

  # sudo ip netns exec ue1 ping 10.45.1.1 -c4
  PING 10.45.1.1 (10.45.1.1) 56(84) bytes of data.
  64 bytes from 10.45.1.1: icmp_seq=1 ttl=64 time=26.6 ms
  64 bytes from 10.45.1.1: icmp_seq=2 ttl=64 time=56.9 ms
  64 bytes from 10.45.1.1: icmp_seq=3 ttl=64 time=45.2 ms
  64 bytes from 10.45.1.1: icmp_seq=4 ttl=64 time=34.9 ms

  --- 10.45.1.1 ping statistics ---
  4 packets transmitted, 4 received, 0% packet loss, time 3002ms
  rtt min/avg/max/mdev = 26.568/40.907/56.878/11.347 ms


iPerf3 
------

In this example, we generate traffic in the uplink direction. To this end, we run an iPerf3 client on the UE side and a server on the network side. UDP traffic will be generated at 10Mbps for 60 seconds. It is important to start the server first, and then the client.

* **Network-side**

Start the iPerf3 server:: 

  iperf3 -s -i 1 

The server listens for traffic coming from the UE. After the client connects, the server prints flow measurements every second.

* **UE-side**

With the network and the iPerf3 server up and running, the client can be run from the UE's machine with the following command:: 

  sudo ip netns exec ue1 iperf3 -c 10.45.1.1 -b 10M -i 1 -t 60  

Traffic will now be sent from the UE to the network. This will be shown in both the server and client consoles. Additionaly, we will observe console traces of the UE and the gNB. 

* **Iperf3 Output**

Example **server** iPerf3 output:: 

  # iperf3 -s -i 1 
  -----------------------------------------------------------
  Server listening on 5201
  -----------------------------------------------------------
  Accepted connection from 10.45.1.2, port 39176
  [  5] local 10.45.1.1 port 5201 connected to 10.45.1.2 port 39184
  [ ID] Interval           Transfer     Bitrate
  [  5]   0.00-1.00   sec  1.18 MBytes  9.91 Mbits/sec                  
  [  5]   1.00-2.00   sec  1.25 MBytes  10.5 Mbits/sec                  
  [  5]   2.00-3.00   sec  1.12 MBytes  9.44 Mbits/sec                  
  [  5]   3.00-4.00   sec  1.17 MBytes  9.85 Mbits/sec                  
  [  5]   4.00-5.00   sec  1.20 MBytes  10.1 Mbits/sec                  
  [  5]   5.00-6.00   sec  1.25 MBytes  10.5 Mbits/sec  

Example **client** iPerf3 output:: 

  # sudo ip netns exec ue1 iperf3 -c 10.45.1.1 -b 10M -i 1 -t 60
  Connecting to host 10.45.1.1, port 5201
  [  5] local 10.45.1.2 port 39184 connected to 10.45.1.1 port 5201
  [ ID] Interval           Transfer     Bitrate         Retr  Cwnd
  [  5]   0.00-1.00   sec  1.31 MBytes  11.0 Mbits/sec    0    119 KBytes       
  [  5]   1.00-2.00   sec  1.12 MBytes  9.44 Mbits/sec    0    132 KBytes       
  [  5]   2.00-3.00   sec  1.25 MBytes  10.5 Mbits/sec    0    132 KBytes       
  [  5]   3.00-4.00   sec  1.12 MBytes  9.44 Mbits/sec    0    132 KBytes       
  [  5]   4.00-5.00   sec  1.25 MBytes  10.5 Mbits/sec    0    132 KBytes       
  [  5]   5.00-6.00   sec  1.12 MBytes  9.44 Mbits/sec    0    132 KBytes      


* **Console Traces**

The following example trace was taken from the **srsUE console** while running the above iPerf3 test:: 

  ---------Signal-----------|-----------------DL-----------------|-----------UL-----------
  rat  pci  rsrp   pl   cfo | mcs  snr  iter  brate  bler  ta_us | mcs   buff  brate  bler
   nr    1     9    0 -1.8u |  27   69   1.3   282k    0%    0.0 |  27   136k    13M    0%
   nr    1     8    0  505n |  27   73   1.3   299k    0%    0.0 |  27    0.0    14M    0%
   nr    1     9    0  499n |  27  n/a   1.2   276k    0%    0.0 |  27   110k    13M    0%
   nr    1     9    0  1.8u |  27   66   1.3   295k    0%    0.0 |  27    3.0    14M    0%
   nr    1     9    0  759n |  27   69   1.3   277k    0%    0.0 |  27    68k    13M    0%
   nr    1     9    0  188n |  27   71   1.3   290k    0%    0.0 |  27    0.0    13M    0%


To read more about the UE console trace metrics, see the `UE User Manual <https://docs.srsran.com/projects/4g/en/latest/usermanuals/source/srsue/source/6_ue_commandref.html#ue-commandref>`_.

The following example trace was taken from the **gNB console** at the same time period as the srsUE trace shown above:: 

           -------------DL----------------|------------------UL--------------------
 pci rnti  cqi  mcs  brate   ok  nok  (%) | pusch  mcs  brate   ok  nok  (%)    bsr
   1 4601   15   27   281k  335    0   0% |  65.5   28    13M  396    0   0%  39.8k
   1 4601   15   27   288k  353    0   0% |  65.5   28    14M  412    0   0%  39.8k
   1 4601   15   27   293k  346    0   0% |  65.5   28    13M  410    0   0%  39.8k
   1 4601   15   27   273k  332    0   0% |  65.5   28    13M  384    0   0%    0.0
   1 4601   15   27   286k  345    0   0% |  65.5   28    14M  414    0   0%    0.0
   1 4601   15   27   288k  349    0   0% |  65.5   28    14M  410    0   0%    0.0



-----

Troubleshooting
***************

Reference clock
===============

If you encounter issues with the srsUE not finding the cell and/or not being able to stay connected it might be due to inaccurate clocks at the RF frontends. Try to use an external 10 MHz reference or use a GPSDO oscillator.


5G QoS Identifier
=================

By default, Open5GS uses 5QI = 9. If the **qos** section is not provided in the gNB config file, the default one with 5QI = 9 will be generated and the UE should connect to the network. If one needs to change the 5QI, please harmonize these settings between gNB and Open5GS config files, as otherwise, a UE will not be able to connect.

-----

Limitations
***********

srsUE
=====

**Multiple TACs**

  - srsUE does not support the use of multiple TACs. Using multple TACs will result in errors parsing NAS messages from the core, resulting in the UE not connecting correctly. 