.. _picocom:

Picocom
#######

.. warning::

  This document is intended to be used as a guide. Variances in firmware and software versions in local setups may require the sample configuration files provided to be changed. As a result please closely follow the specific users guides of your RU in conjunction with this guide.

Overview
********

This guide provides further details on connecting the srsRAN CU/DU to an RU using the the ORAN 7.2 split. Specifically, we discuss the Picocom PC802SCB.  

The RU is based on a PC802 Small Cell Development Board (PC802SCB) and an ADI ADRV9029BBCZ 4T4R RFIC subsystem, it is capable of up to 100MHz 4T4R. The PC802SCB is a flexible 5G NR development platform for evaluating the PC802 for different 
small cell use cases, including as a split 7.2 O-RU. You can read more about it `here <https://picocom.com/products/boards/>`_.  

.. note::

  The PC802SCB is not a deployment ready commercial grade O-RU, but many commercial O-RUs are based on the PC802 platform. 

-----

Configuration
*************

.. tip:: 
  
  For the most up-to-date configuration changes, troubleshooting and information on potential issues check the `GitHub Discussions <https://github.com/srsran/srsRAN_Project/discussions>`_ 

CU/DU
=====

A sample configuration file for the DU can be downloaded from `here <https://github.com/srsran/srsRAN_Project/blob/main/configs/gnb_ru_picocom_scb_tdd_n78_20mhz.yml>`_. 

The following excerpt shows how the DU is configured to communicate with the RU: 

.. code-block:: yaml

    ru_ofh:
      t1a_max_cp_dl: 350                                              # Maximum T1a on Control-Plane for Downlink in microseconds.
      t1a_min_cp_dl: 250                                              # Minimum T1a on Control-Plane for Downlink in microseconds.
      t1a_max_cp_ul: 250                                              # Maximum T1a on Control-Plane for Uplink in microseconds.
      t1a_min_cp_ul: 150                                              # Minimum T1a on Control-Plane for Uplink in microseconds.
      t1a_max_up: 200                                                 # Maximum T1a on User-Plane in microseconds.
      t1a_min_up: 80                                                  # Minimum T1a on User-Plane in microseconds.
      ta4_max: 300                                                    # Maximum Ta4 on User-Plane in microseconds.
      ta4_min: 10                                                     # Minimum Ta4 on User-Plane in microseconds.
      is_prach_cp_enabled: false                                      # Configures if Control-Plane messages should be used to receive PRACH messages.
      compr_method_ul: bfp                                            # Uplink compression method.
      compr_bitwidth_ul: 9                                            # Uplink IQ samples bitwidth after compression.
      compr_method_dl: bfp                                            # Downlink compression method.
      compr_bitwidth_dl: 9                                            # Downlink IQ samples bitwidth after compression.
      compr_method_prach: bfp                                         # PRACH compression method.
      compr_bitwidth_prach: 9                                         # PRACH IQ samples bitwidth after compression.
      iq_scaling: 1.0                                                 # IQ samples scaling factor applied before compression, should be a positive value smaller than 10.
      cells:
        - network_interface: enp1s0f0                                 # Ethernet interface name used to communicate with the RU.
          ru_mac_addr: ce:fc:6c:09:a6:cd                              # RU MAC address.
          du_mac_addr: 80:61:5f:0d:df:aa                              # DU MAC address.
          vlan_tag_cp: 3                                              # VLAN tag value for C-Plane.
          vlan_tag_up: 3                                              # VLAN tag value for U-Plane.
          prach_port_id: [0]                                          # PRACH eAxC port value.
          dl_port_id: [0]                                             # Downlink eAxC port values.
          ul_port_id: [0]                                             # Uplink eAxC port values.

To expand on this, the following parameters are set in the ``cells`` field:

- ``network_interface`` : Network interface used to send the OFH packets.
- ``ru_mac_addr`` : MAC address of the RU.
- ``du_mac_addr`` : MAC address of the interface used by the DU for OFH traffic.
- ``vlan_tag_up/vlan_tag_cp`` : VLAN identifier, should be set to the value configured in the RU/switch settings.

In the ``cell_cfg`` section of the configuration, the ``prach`` and ``tdd_ul_dl_cfg`` fields must also be configured correctly. The following excerpt shows this: 

.. code-block:: yaml 

  prach:
    prach_config_index: 159                                       # PRACH configuration index.
    prach_root_sequence_index: 1                                  # PRACH root sequence index.
    zero_correlation_zone: 0                                      # Zero correlation zone.
    prach_frequency_start: 0                                      # Offset in PRBs of lowest PRACH transmission occasion in frequency domain respective to PRB 0.
  tdd_ul_dl_cfg:
    nof_dl_slots: 7
    nof_ul_slots: 2

It is important to check these fields as their values may change based on the RU being used. 

RU 
=====

The first step will be to power-on the board and ensure it is connected correctly to the PC running the CU/DU. Next, log in to the RU via SSH. Once the RU has been accessed correctly via the terminal, 
it can be configured and connected to the CU/DU and OFH packets can be sent between the two. 


.. note:: 

    This configuration is relevant to firmware v3.0.0. Other firmware versions may require different configurations. For more information on this reference the relevant documentation from Picocom. 

Configuration
-------------

The RU must first be configured so that the relevant values match across the DU and RU. 

RU OFH related parameters can be found in the file *rf_init_req.json* in this path */home/user/PC-003001-LS/npu/oru_oam/inputs*. Inside this JSON file there is a property called ``ecpri_cu_plane_parameters``:

.. code-block:: json

    "ecpri_cu_plane_params" : {
        "is_static_compress" : 1,
        "compress_method" : 1, 
        "compress_iq_width" : 9,
        "c_plane_enable": 1,
        "ul_padding_enable": 1,
        "fhm_via_sectionid_enable": 0,
        "cu_mac_check_enable": 0,
        "eAxC_id_bit_alloc": 0,  
        "du_port_id" : 0,
        "bandsector_id" : 0,
        "cc_id" : 0,
        "ru_port_dl": [0, 1, 2, 3],
        "ru_port_ul_nonprach": [0, 1, 2, 3],
        "ru_port_ul_prach": [0, 1, 2, 3]
    },

Make sure that Control-Plane is enabled (``"c_plane_enable": 1,``) and that the rest of the parameters match those in the DU configuration.

In this file the Ethernet connection parameters can be found in the property ``transport_parameters``:

.. code-block:: json

    "transport_params" : {
        "transport_session_type" : 0,
        "vlan_id" : 4000,
        "l2_mtu" : 9000,
        "odu_mac_addr" : ["0x8C","0x1F","0x64","0xB4","0xC0","0x03"],
        "oru_mac_addr" : ["0x8C","0x1F","0x64","0xB4","0xC1","0xF2"]
    },
        
Adjust the ``vlan_id``, ``odu_mac_addr``, ``oru_mac_addr`` and ``l2_mtu`` to match the DU configuration.

RU PRACH related parameters can be found in the file *prach_req.json* in this path */home/user/PC-003001-LS/npu/oru_oam/inputs*. In this file, check the property ``prach_cu_plane_params``:

.. code-block:: json

    "prach_cu_plane_params" : {
        "is_static_compress" : 1,
        "compress_method" : 1,
        "compress_iq_width" : 9,
        "c_plane_enable": 1,
        "param_source": 0
    }

Make sure that the settings matches the DU settings.

Another important section of this file is ``common_params``:

.. code-block:: json

    "common_params" : {
        "bandwidth" : 100000,
        "dl_frame_start_offset" : 0,
        "ul_frame_start_offset" : -13021,
        "dl_wave_delay" : 918,
        "ul_wave_delay" : 1005,
        "scs_hz" : 30000,
        "cp_type" : 0,
        "num_tx_port" : 4,
        "num_rx_port" : 4,
        "ul_fft_dynamic_scaling_enable" : 1,
        "slotnum_txrx_pattern" : 10,
        "slotconfig": ["0xf0000000","0xf0000000","0xf0000000","0xf0000000","0xf0000000","0xf0000000","0xf0000000","0xf55aa000","0xf5555555","0xf5555555"]
    },

Make sure that the ``slotnum_txrx_pattern``, ``cp_type``, ``scs_hz`` and ``bandwidth`` parameters matches the DU configuration. The number of antennas can be configured to 4, as the DU will ask the data for the antennas that it configures.

Also pay attention to the ``sync_scheme_params`` property:

.. code-block:: json

    "sync_scheme_params" : {
        "sync_source" : 3,
        "is_pc802_ctrl_vcxo" : 2,
        "enable_pc802_sw_filtering_on_1ppsin" : 1,
        "pps_tod_sync_threshold" : 100,
        "count_pps_insync": 10,
        "freq_adj_rate_factor": 4,
        "pps_tod_outsync_threshold": 100,
        "gpio_pps_out": "0xFF"
    },

Property ``sync_source`` should be configured to use PTP.

If the RSRP detected by the UE is low, is possible to increase it by updating ``dl_amplitude_scale`` property. Check Picocom documentation for valid values. For reference, srsRAN Project uses the following by default:

.. code-block:: json

	"dl_amplitude_scale" : 65535.

To enable the output metrics of the RU, make sure OAM is sending the corresponding command to the PC802. The configuration of the messages sent to the PC802 can be found in the file *config.ini* in */home/user/PC-003001-LS/npu/oru_oam*. For example:

.. code-block:: ini

	[MSG_REQ_LIST]
	msg_id=0       	    #rf init req
	msg_id=300     	    #p19 req
	msg_id=4       	    #prach config req
	msg_id=1            #start req
	msg_id=108          #status
	msg_id=109     	    #measurement status update req
	msg_id=110     	    #measurement counter read req
	#msg_id=2      	    #stop req
	#msg_id=65280       #dl scale update

Also check the file *measurement_status_update_req_list.json* and *measurement_counter_read_req.json* in *inputs* folder. 

As an example the contents of *measurement_counter_read_req.json* should read:

.. code-block:: json

	{
	    "measurement_counter_read_req" : {
		"measurement_group" : 0,
		"object_unit" : 0,
		"report_info" : 0
	    }
	}

And contents of *measurement_status_update_req_list.json* should read:

.. code-block:: json

	{
	    "measurement_status_update_req_list" : {
		"num_of_msg" : 2,
		"measurement_status_update_msg" : [
		    {
		        "measurement_group" : 0,
		        "measurement_interval" : 1,
		        "active" : 1,
		        "object_unit" : 0,
		        "report_info" : 0
		    },
		    {
		        "measurement_group" : 1,
		        "measurement_interval" : 1,
		        "active" : 1,
		        "object_unit" : 0,
		        "report_info" : 0
		    }
		]
	    }
	}

Running the RU
--------------

Once the RU has been correctly configured, the next step will be to start the RF part of the board. To do this, navigate to the RF folder and run the relevant script with ``sudo``: 

.. code-block:: bash 

    cd PC-003001-LS/npu/RFICDriver/
    sudo ./run.sh 

You should then see the following output or similar:

.. code-block:: bash 

    Value is 2, currently Board Type is scb_x3
    Run the reset_rfic
    Export GPIO 3-2 (418) to userspace.
    ...
    ...

    adi_board_adrv9025_JesdBringup 1079, adrv9025LinkStatus = 0
    ADRV9025 TX deframer status = 18
    adi_board_adrv9025_Program_Phase2 1678, adrv9025 RX LinkStatus 4 = 6
    main 102
    Reg 6a89 read back: 25
    RX gain index: 0
    RSSI level: 0

The kernel module must then be loaded. This can be done from the home directory: 

.. code-block:: bash 

    sudo insmod pcsc.ko 

To check that it has been loaded correctly, run the following command: 

.. code-block:: bash 

    ip a 

You should see the following output or similar if the kernel module has been loaded correctly: 

.. code-block:: bash 

    ...
    8: pcsce0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
        link/ether 56:69:eb:b9:65:0b brd ff:ff:ff:ff:ff:ff

Next, go to the ``ru_oam`` folder and start the ``oam_manager`` process:

.. code-block:: bash 

    cd PC-003001-LS/npu/ru_oam/
    sudo ./oam_manager

The following output should be observed: 

.. code-block:: bash 

    GIT_BRANCH=master;
    GIT_BRANCH=f8233eb84a73f4dea67ec2a118ada4935507603d;
    [Initial oam messages sequence sending]:
    [#################################################################################################### ][100%][-]
    <start oam interactive operation>
    [oam@operation]#

The PTP process now needs to be started on the board. To do this, open two new terminals via SSH. In the first terminal, run the following command: 

.. code-block:: bash 

    cd PC-003001-LS/npu/linuxptp-3.1.1/
    sudo ./ptp4l_run.sh


You should then see: 

.. code-block:: 

    ptp4l[23:24: 2.410]: selected /dev/ptp1 as PTP clock
    ptp4l[23:24: 2.453]: port 1: INITIALIZING to LISTENING on INIT_COMPLETE
    ptp4l[23:24: 2.453]: port 0: INITIALIZING to LISTENING on INIT_COMPLETE
    ptp4l[23:24: 2.523]: port 1: new foreign master 000580.fffe.0837cd-20
    ptp4l[23:24: 2.789]: selected best master clock 000580.fffe.0837cd
    ptp4l[23:24: 2.790]: updating UTC offset to 37
    ptp4l[23:24: 2.790]: port 1: LISTENING to UNCALIBRATED on RS_SLAVE
    ptp4l[23:24: 3.554]: port 1: UNCALIBRATED to SLAVE on MASTER_CLOCK_SELECTED
    ptp4l[23:24: 3.976]: rms 1266036736054421504 max 1688048981730611712 freq   -445 +/- 503 delay   193 +/-   2
    ptp4l[23:24: 5.101]: rms  153 max  274 freq   -315 +/- 263 delay   184 +/-   4
    ptp4l[23:24: 6.226]: rms  125 max  164 freq	+35 +/-  15 delay   194 +/-   1
    ... 
    ...
    ...
    ptp4l[23:24:14.101]: rms	2 max	3 freq	-39 +/-   3 delay   193 +/-   0

In the second terminal, run the ``phc2sys`` script: 

.. code-block:: bash 

    cd PC-003001-LS/npu/linuxptp-3.1.1/
    sudo ./phc2sys -s /dev/ptp1 -c CLOCK_REALTIME -w -l 7 -n 24 -m

This will give the following output: 

.. code-block:: bash 

    phc2sys[23:25:14.797]: config item (null).clock_servo is 0
    phc2sys[23:25:14.798]: config item (null).kernel_leap is 1
    phc2sys[23:25:14.798]: config item (null).sanity_freq_limit is 200000000
    phc2sys[23:25:14.799]: config item (null).pi_proportional_const is 0.700000
    phc2sys[23:25:14.799]: config item (null).pi_integral_const is 0.300000
    phc2sys[23:25:14.800]: config item (null).pi_proportional_scale is 0.000000
    phc2sys[23:25:14.800]: config item (null).pi_proportional_exponent is -0.300000
    phc2sys[23:25:14.800]: config item (null).pi_proportional_norm_max is 0.700000
    phc2sys[23:25:14.801]: config item (null).pi_integral_scale is 0.000000
    phc2sys[23:25:14.803]: config item (null).pi_integral_exponent is 0.400000
    phc2sys[23:25:14.803]: config item (null).pi_integral_norm_max is 0.300000
    phc2sys[23:25:14.803]: config item (null).step_threshold is 0.000000
    phc2sys[23:25:14.804]: config item (null).first_step_threshold is 0.000020
    phc2sys[23:25:14.804]: config item (null).max_frequency is 900000000
    phc2sys[23:25:14.804]: config item (null).servo_offset_threshold is 0
    phc2sys[23:25:14.805]: config item (null).servo_num_offset_values is 10
    phc2sys[23:25:14.805]: PI servo: sync interval 1.000 kp 0.700 ki 0.300000
    phc2sys[23:25:14.805]: ioctl PTP_SYS_OFFSET_PRECISE: Operation not supported
    phc2sys[23:25:14.806]: ioctl PTP_SYS_OFFSET_EXTENDED: Operation not supported
    phc2sys[23:25:14.806]: config item (null).pi_proportional_const is 0.700000
    ...
    ...
    phc2sys[23:25:14.810]: config item (null).servo_num_offset_values is 10
    phc2sys[23:25:14.810]: PI servo: sync interval 1.000 kp 0.700 ki 0.300000
    phc2sys[23:25:14.811]: config item (null).domainNumber is 24
    phc2sys[23:25:14.811]: config item (null).transportSpecific is 0
    phc2sys[23:25:14.811]: config item (null).uds_address is '/var/run/ptp4l'
    phc2sys[23:25:15.812]: CLOCK_REALTIME phc offset -9155196481971402 s0 freq  	+0 delay   9520
    phc2sys[22:31:53.299]: CLOCK_REALTIME phc offset -9155196482007884 s1 freq  -36468 delay  10280
    phc2sys[22:31:54.301]: CLOCK_REALTIME phc offset  	1539 s2 freq  -34929 delay   8201
    ...
    ...
    phc2sys[22:31:57.302]: CLOCK_REALTIME phc offset   	856 s2 freq  -34994 delay   9361
    K_REALTIME phc offset  	-167 s2 freq  -35761 delay  10161

This will need to be left running for 1 to 2 minutes so that the PTP process can stabilize.

-----

Initializing and connecting to the network
******************************************

Initializing and connecting to the network is done in the same way as outlined in the general 7.2 RU guide. 

Initializing the network
========================

The following steps should be taken to initialize the network: 

Ensure the RU is started and has PTP lock (see above).

Run the CU/DU, making sure that the PTP sync between the DU and the Falcon switch is successful as previously outlined.  

.. code-block:: bash

    sudo ./gnb -c gnb_ru_picocom_scb_tdd_n78_20mhz.yml

If the DU connects to the RU successfully, you will see the following output: 

.. code-block:: bash

  --== srsRAN gNB (commit 78238fd) ==--

  Connecting to AMF on 127.0.0.5:38412
  Initializing the Open Fronthaul Interface for sector#0: ul_compr=[BFP,9], dl_compr=[BFP,9], prach_compr=[BFP,9], prach_cp_enabled=false, downlink_broadcast=false
  Cell pci=1, bw=20 MHz, 4T4R, dl_arfcn=625000 (n78), dl_freq=3375.0 MHz, dl_ssb_arfcn=625056, ul_freq=3375.0 MHz

  ==== gNodeB started ===
  Type <t> to view trace

Once the RU is started and it detects the PTP, a CSV file is created in */home/user/PC-003001-LS/npu/oru_oam*. It prints the KPIs every second with this format, you should see the following or similar:

.. code-block:: console

	0,TX_TOTAL,2023-03-27T22:30:08+00:00,2023-03-27T22:30:09+00:00,RU,30400
	1,TX_TOTAL_C,2023-03-27T22:30:08+00:00,2023-03-27T22:30:09+00:00,RU,0
	0,RX_TOTAL,2023-03-27T22:30:08+00:00,2023-03-27T22:30:09+00:00,RU,56000
	1,RX_ON_TIME,2023-03-27T22:30:08+00:00,2023-03-27T22:30:09+00:00,RU,0
	2,RX_EARLY,2023-03-27T22:30:08+00:00,2023-03-27T22:30:09+00:00,RU,31812
	3,RX_LATE,2023-03-27T22:30:08+00:00,2023-03-27T22:30:09+00:00,RU,24188
	4,RX_ON_TIME_C,2023-03-27T22:30:08+00:00,2023-03-27T22:30:09+00:00,RU,0
	5,RX_EARLY_C,2023-03-27T22:30:08+00:00,2023-03-27T22:30:09+00:00,RU,0
	6,RX_LATE_C,2023-03-27T22:30:08+00:00,2023-03-27T22:30:09+00:00,RU,0

Connecting to the network
=========================

You can now connect a UE to the network. This can be done using e.g. a COTS UE. See the main RU guide for details on this.