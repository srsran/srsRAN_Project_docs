.. _testmode:

srsRAN gNB(-DU) Load Testing
#######################


Introduction
************

In this tutorial, we will guide you through the process of load testing the srsRAN Project gNB(-DU) application without the need for specific hardware, via parameters available within the configuration file.

The ``ru_dummy`` option in the gNB configuration allows users to emulate the RU and focus exclusively on testing the DU, by excluding the OFH layers. The RU Emulator (``ru_emu``) can be used to simulate traffic 
sent and received by an O-RU in a split 7.2 configuration, while also allowing you to monitor key performance indicators (KPIs). 


For scenarios without a core network, the ``no_core`` flag in the gNB configuration allows the gNB(-DU) to operate without a physical core network.

The ``testmode`` feature in the gNB application was developed to evaluate the performance of the srsRAN gNB(-DU) on specific hardware. This 
function emulates single or multiple UEs, simulating traffic  across layers such as MAC, PHY, and OFH. By replicating traffic from the CU and RU to the DU, 
``testmode`` provides an effective way to assess and optimize system performance. Integrated directly into the gNB application, ``testmode`` requires no additional 
builds beyond the gNB. 

Detailed explanations of these scenarios are provided in the following sections. For detailed information on specific configuration parameters and usage of these modes, refer to the 
srsRAN Project :ref:`Configuration Reference <manual_config_ref>`.

-----

Using ``ru_dummy``
******************

In case you want to do a load test without a physical or emulated RU you can use the ``ru_dummy`` config option in the gNB config. This will exclude the OFH layer from the test because no data 
is sent over the network. To use the ``ru_dummy`` parameter add the following section to your gNB config file:
    
    .. code-block:: yaml

      ru_dummy:
        dl_processing_delay: 1
        time_scaling: 1

-----

Using ``ru_emu``
****************

The RU Emulator is an extra tool that needs to be built separately from the gNB application. To build the RU Emulator use the following commands from inside the srsRAN Project repository:

  .. code-block:: bash

    mkdir build && cd build
    cmake ..
    cd apps/examples/ofh
    make -j $(nproc)

In case you want to run the RU Emulator using DPDK use the following cmake command instead:

  .. code-block:: bash

    cmake -ENABLE_DPDK=ON ..

.. note:: 

  Building with DPDK is not a requirement for using ``ru_emu``    

Create a new configuration file called ``emu.yaml`` with the following content:

  .. code-block:: yaml

    log:
      filename: /tmp/ru_emu.log
      level: warning

    ru_emu:
        cells:
        - bandwidth: 100                          # Bandwidth of the cell
          ru_mac_addr: 00:33:22:33:00:11
          du_mac_addr: 00:33:22:33:00:66
          enable_promiscuous: false
          vlan_tag: 33
          dl_port_id: [0, 1, 2, 3]
          ul_port_id: [0, 1, 2, 3]
          prach_port_id: [4, 5]
          compr_method_ul: "bfp"
          compr_bitwidth_ul: 9
          t2a_max_cp_dl: 470
          t2a_min_cp_dl: 350
          t2a_max_cp_ul: 200
          t2a_min_cp_ul: 90
          t2a_max_up: 345
          t2a_min_up: 70
    
    # dpdk:
    #   eal_args: "--lcores (0-1)@(0-15)"

Adjust the above parameters to match your configuration. If you want to use DPDK, provide the Bus Device Function (BDF) of the NIC in the ``network_interface`` field. The BDF can be found 
using the ``dpdk-devbind.py -s`` command. Also, uncomment the ``dpdk`` section and provide the correct ``eal_args`` arguments.

Use the following command to start the RU Emulator:

  .. code-block:: bash
    
    sudo ./ru_emulator -c emu.yaml

You should see the following output:

  .. code-block:: bash

    Running. Waiting for incoming packets...
    |   TIME   | ID  |  RX_TOTAL   | RX_ON_TIME  |  RX_EARLY   |   RX_LATE   |   RX_SEQ_ERR    | RX_ON_TIME_C  |  RX_EARLY_C   |   RX_LATE_C   |  RX_SEQ_ERR_C   | RX_ON_TIME_C_U |  RX_EARLY_C_U  |  RX_LATE_C_U   | RX_SEQ_ERR_C_U  | RX_SEQ_ERR_PRACH | RX_CORRUPT  | RX_ERR_DROP |  TX_TOTAL   |
    | 15:26:48 |  0  |      0      |      0      |      0      |      0      |     0/0/0/0     |       0       |       0       |       0       |     0/0/0/0     |       0        |       0        |       0        |        0        |       0/0       |      0      |      0      |      0      |
    | 15:26:49 |  0  |      0      |      0      |      0      |      0      |     0/0/0/0     |       0       |       0       |       0       |     0/0/0/0     |       0        |       0        |       0        |        0        |       0/0       |      0      |      0      |      0      |
    | 15:26:50 |  0  |      0      |      0      |      0      |      0      |     0/0/0/0     |       0       |       0       |       0       |     0/0/0/0     |       0        |       0        |       0        |        0        |       0/0       |      0      |      0      |      0      |
    | 15:26:51 |  0  |      0      |      0      |      0      |      0      |     0/0/0/0     |       0       |       0       |       0       |     0/0/0/0     |       0        |       0        |       0        |        0        |       0/0       |      0      |      0      |      0      |
    | 15:26:52 |  0  |      0      |      0      |      0      |      0      |     0/0/0/0     |       0       |       0       |       0       |     0/0/0/0     |       0        |       0        |       0        |        0        |       0/0       |      0      |      0      |      0      |
    | 15:26:53 |  0  |      0      |      0      |      0      |      0      |     0/0/0/0     |       0       |       0       |       0       |     0/0/0/0     |       0        |       0        |       0        |        0        |       0/0       |      0      |      0      |      0      |
    | 15:26:54 |  0  |      0      |      0      |      0      |      0      |     0/0/0/0     |       0       |       0       |       0       |     0/0/0/0     |       0        |       0        |       0        |        0        |       0/0       |      0      |      0      |      0      |
    | 15:26:55 |  0  |      0      |      0      |      0      |      0      |     0/0/0/0     |       0       |       0       |       0       |     0/0/0/0     |       0        |       0        |       0        |        0        |       0/0       |      0      |      0      |      0      |
    | 15:26:56 |  0  |      0      |      0      |      0      |      0      |     0/0/0/0     |       0       |       0       |       0       |     0/0/0/0     |       0        |       0        |       0        |        0        |       0/0       |      0      |      0      |      0      |
    | 15:26:57 |  0  |      0      |      0      |      0      |      0      |     0/0/0/0     |       0       |       0       |       0       |     0/0/0/0     |       0        |       0        |       0        |        0        |       0/0       |      0      |      0      |      0      |
    | 15:26:58 |  0  |      0      |      0      |      0      |      0      |     0/0/0/0     |       0       |       0       |       0       |     0/0/0/0     |       0        |       0        |       0        |        0        |       0/0       |      0      |      0      |      0      |
    | 15:26:59 |  0  |      0      |      0      |      0      |      0      |     0/0/0/0     |       0       |       0       |       0       |     0/0/0/0     |       0        |       0        |       0        |        0        |       0/0       |      0      |      0      |      0      |
    | 15:27:00 |  0  |      0      |      0      |      0      |      0      |     0/0/0/0     |       0       |       0       |       0       |     0/0/0/0     |       0        |       0        |       0        |        0        |       0/0       |      0      |      0      |      0      |
    | 15:27:01 |  0  |      0      |      0      |      0      |      0      |     0/0/0/0     |       0       |       0       |       0       |     0/0/0/0     |       0        |       0        |       0        |        0        |       0/0       |      0      |      0      |      0      |

The above KPIs are indicating the KPIs of the RU Emulator. The RU Emulator is now running and waiting for incoming packets. Once an RU is connected you should see the ``*_ON_TIME_*`` counters 
increase. The RU is operating properly if you do not see any late, early or err packets.

-----

Using ``no_core``
*****************

In case you want to emulate the core network in cases where no 5G core is available, you can use the ``no_core`` flag in the gNB config. To use the ``no_core`` flag add the following section to your gNB config:
    
  .. code-block:: yaml

    cu_cp:
      amf:
        no_core: false

-----

Using ``testmode``
******************

Once an RU and a core network are in place you can start using ``testmode``. A sample configuration file can also be found in `srsRAN_Project/configs` within 
the srsRAN Project source files: 

  .. code-block:: yaml

    test_mode:
      test_ue:
        rnti: 0x44
        ri: 1 # Set to 2 or 4 for 2 layer or 4 layer MIMO operation
        cqi: 15
        nof_ues: 1
        pusch_active: true
        pdsch_active: true
  
This config will emulate a single UE with ``RNTI`` = 0x44, ``CQI`` is set to 15 and ``RI`` to 1. 

Configuration files can be concatenated when running the gNB(-DU), which means users can easily test various configurations without having to modify their base configuration. For this example, the configuration above 
will be concatenated with the example configuration ``gnb_ru_ran550_tdd_n78_100mhz_4x2.yml`` which can be found in ``srsRAN_Project/configs``. This will allow the RU to be tested without a physical UE being connected. 
This ability extends to other frontends such as USRPs, and also ZMQ.

To run the described scenario, the following command can be used: 

  .. code-block:: bash 

    sudo ./apps/gnb/gnb -c gnb_ru_ran550_tdd_n78_100mhz_4x2.yml -c testmode.yml

You should then see the following output:

  .. code-block:: bash

    --== srsRAN gNB (commit f41c1db4c3) ==--

    Warning: With the given prach_frequency_start=0, the PRACH opportunities overlap with the PUCCH resources/guardband in prbs=[0, 8). Some interference between PUCCH and PRACH interference should be expected
    Cell pci=1, bw=100 MHz, 4T2R, dl_arfcn=637212 (n78), dl_freq=3558.18 MHz, dl_ssb_arfcn=634464, ul_freq=3558.18 MHz

    Initializing the Open Fronthaul Interface for sector#0: ul_compr=[BFP,9], dl_compr=[BFP,9], prach_compr=[BFP,9], prach_cp_enabled=false, downlink_broadcast=false
    ==== gNB started ===
    Type <h> to view help

             |--------------------DL---------------------|-------------------------UL------------------------------
    pci rnti | cqi  ri  mcs  brate   ok  nok  (%)  dl_bs | pusch  rsrp  mcs  brate   ok  nok  (%)    bsr     ta  phr
      1 0x44 |  15 1.0   28   1.0G 1539    0   0%    10M |  99.9 -99.9   28    75M  400    0   0%  81.5M      0  n/a
      1 0x44 |  15 1.0   28   1.0G 1546    0   0%    10M |  99.9 -99.9   28    75M  400    0   0%  81.5M      0  n/a
      1 0x44 |  15 1.0   28   1.0G 1541    0   0%    10M |  99.9 -99.9   28    75M  400    0   0%  81.5M      0  n/a
      1 0x44 |  15 1.0   28   1.0G 1547    0   0%    10M |  99.9 -99.9   28    75M  399    0   0%  81.5M      0  n/a
      1 0x44 |  15 1.0   28   1.0G 1543    0   0%    10M |  99.9 -99.9   28    76M  401    0   0%  81.5M      0  n/a
      1 0x44 |  15 1.0   28   1.0G 1542    0   0%    10M |  99.9 -99.9   28    75M  400    0   0%  81.5M      0  n/a
      1 0x44 |  15 1.0   28   1.0G 1549    0   0%    10M |  99.9 -99.9   28    75M  400    0   0%  81.5M      0  n/a
      1 0x44 |  15 1.0   28   1.0G 1542    0   0%    10M |  99.9 -99.9   28    75M  400    0   0%  81.5M      0  n/a
      1 0x44 |  15 1.0   28   1.0G 1546    0   0%    10M |  99.9 -99.9   28    75M  399    0   0%  81.5M      0  n/a
      1 0x44 |  15 1.0   28   1.0G 1546    0   0%    10M |  99.9 -99.9   28    75M  400    0   0%  81.5M      0  n/a
      1 0x44 |  15 1.0   28   1.0G 1548    0   0%    10M |  99.9 -99.9   28    76M  401    0   0%  81.5M      0  n/a

For more information about the test mode please refer to the srsRAN Project `Configuration Reference <https://docs.srsran.com/projects/project/en/latest/user_manuals/source/config_ref.html>`_. 
