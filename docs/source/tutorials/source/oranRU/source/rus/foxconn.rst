.. _foxconn:

Foxconn RPQN-(48/78)00(E/I)
################

.. warning::

  This document is intended to be used as a guide. Variances in firmware and software versions in local setups may require the sample configuration files provided to be changed. As a result please closely follow the specific users guides of your RU in conjunction with this guide.

Overview
********

This guide provides further details on connecting the srsRAN CU/DU to an RU using the the ORAN 7.2 split. Specifically, we discus the Foxconn RPQN family of devices.
They are available in various flavors, hence different model numbers:

- With and without external antenna (the E letter at the end stands for external antenna and the I for internal). 
- For different bands (the 78 means n78 for Europe and 48 means band n48 for US markets).
- There is also the "xx01" series that apperantly has some further differences in RF characterisics.

.. note::

  Please refer to the Foxconn User Guide provided by the distributor for up-to-date configuration and usage guidelines.

-----

Configuration
*************

.. tip:: 
  
  For the most up-to-date configuration changes, troubleshooting and information on potential issues check the `GitHub Discussions <https://github.com/srsran/srsRAN_Project/discussions>`_ 

CU/DU
=====

A sample configuration file for the DU can be downloaded from `here <https://github.com/srsran/srsRAN_Project/blob/main/configs/gnb_ru_rpqn4800e_tdd_n78_20mhz_2x2.yml>`_. This configuration is **specific** to the firmware version of the RU (v3_1_13q_551p1)
being used for this guide. As a result, you may need to modify this slightly for your local setup. 

The following excerpt shows how the DU is configured to communicate with the RU: 

.. code-block:: yaml

  ru_ofh:
    t1a_max_cp_dl: 420
    t1a_min_cp_dl: 250
    t1a_max_cp_ul: 420
    t1a_min_cp_ul: 250
    t1a_max_up: 196
    t1a_min_up: 80
    ta4_max: 500
    ta4_min: 25
    is_prach_cp_enabled: true
    ignore_ecpri_payload_size: true
    compr_method_ul: bfp
    compr_bitwidth_ul: 9
    compr_method_dl: bfp
    compr_bitwidth_dl: 9
    compr_method_prach: bfp
    compr_bitwidth_prach: 9
    enable_ul_static_compr_hdr: false
    enable_dl_static_compr_hdr: false
    iq_scaling: 1.0
    cells:
      - network_interface: xxxx          # Ethernet interface name used to communicate with the RU.
        ru_mac_addr: 6c:ad:ad:xx:xx:xx   # RU MAC address.
        du_mac_addr: 80:61:5f:xx:xx:xx   # DU MAC address.
        vlan_tag_cp: 2                   # VLAN tag value for CP.
        vlan_tag_up: 2                   # VLAN tag value for UP.    
        prach_port_id: [4, 5, 6, 7]      # PRACH eAxC port values.
        dl_port_id: [0, 1]               # Downlink eAxC port values.
        ul_port_id: [0, 1, 2, 3]         # Uplink eAxC port values.

To expand on this, the following parameters are set in the ``cells`` field:

- ``network_interface`` : Network interface used to send the OFH packets.
- ``ru_mac_addr`` : MAC address of the RU.
- ``du_mac_addr`` : MAC address of the interface used by the DU for OFH traffic.
- ``vlan_tag_up/vlan_tag_cp`` : VLAN identifier, should be set to the value configured in the RU/switch settings.

RU 
=====

Refer to the Foxconn User Guide documentation to apply the following configuration changes so that they match your local setup. The following information is purely a guide and may not work for your specific set up. 

The RU can operate and has been tested in bandwidths between 20 to 100 MHz, in SISO mode as well
as in 2x2 or 4x4 MIMO mode. In ideal conditions (i.e., in a conducted setup) maximum data rate can be achieved and 256-QAM are supported for both downlink and uplink tranmssions.
We've found that the best signal quality is achieved with 90 MHz bandwidth due to some filter roll-off in the RU.

All configuration values of the RU can be set/modified in the `RRHconfig_xran.xml` file. The file can usually be found in the `/home/root/sdcard/` folder but has moved to `/home/root` in more recent firmware versions.

Below are the most critical values to be set and the ones that differ from the RU's default configuration values:

- ``RRH_DST_MAC_ADDR`` : The MAC address of the DU must be configured in the RU for Control-Plane and User-Plane traffic. Note that the ``RRH_SRC_MAC_ADDR`` is usually not read from the config file and will be auto-set to the MAC address of the 10G interface during boot.
- ``RRH_EN_EAXC_ID`` : Set to ``0`` to map RU port ID 0, 1, 2, 3 to PDSCH/PUSCH and 4, 5, 6, 7 to PRACH.
- ``RRH_CMPR_TYPE = 1, 1`` : Set to ``1, 1`` to enable BFP compression for PDSCH/PUSCH and PRACH.
- ``RRH_C_PLANE_VLAN_TAG/RRH_U_PLANE_VLAN_TAG`` : Set this to a value of your choice, we usually use the same VLAN for both.
- ``RRH_MAX_PRB`` : The channel bandwidth. Set this to e.g., ``51`` for a 20 MHz cell, to ``245`` for 90 MHz and ``273`` for a 100 MHz cell.
- ``RRH_LO_FREQUENCY_KHZ`` : The center frequency of the cell in kHz, set to e.g., ``3600000, 0`` to radiate at 3.6 GHz (ARFCN 640000).

The full configuration example file we used for this set up can be found :download:`here <.configs/foxconn_rrh_config.txt>`. In this config we are configuring the RU for 20 MHz.

After the configuration file has been updated the RU firmware can be initialized by running the ``./init_rrh_config_enable_cuplane`` script on the console. Observe the output, verify that
the values have been read from the config file correctly and that the RU locks the PTP sync. For this the init script should print ``ptp locked: state=3`` at the end of the execution.

-----

Initializing and connecting to the network
******************************************

Initializing and connecting to the network is done in the same way as outlined in the general 7.2 RU guide. 

Initializing the network
========================

The following steps should be taken to initialize the network: 

1. Ensure the RU is started and has PTP lock (see above).

2. Run the CU/DU, making sure that the PTP sync between the DU and the Falcon switch is successful as previously outlined.  

    .. code-block:: bash

      sudo ./gnb -c gnb_ru_rpqn4800e_tdd_n78_20mhz.yml

  If the DU connects to the RU successfully, you will see the following output: 

    .. code-block:: bash

      --== srsRAN gNB (commit 96f185389) ==--

      Connecting to AMF on 127.0.0.5:38412
      Initializing the Open Fronthaul Interface for sector#0: ul_compr=[BFP,9], dl_compr=[BFP,9], prach_compr=[BFP,9], prach_cp_enabled=true, downlink_broadcast=false
      Cell pci=1, bw=20 MHz, 2T2R, dl_arfcn=640000 (n78), dl_freq=3600.0 MHz, dl_ssb_arfcn=639648, ul_freq=3600.0 MHz

      ==== gNodeB started ===
      Type <t> to view trace

3. If you have the DU running you can go back to the SSH console on the RU and check that the fronthaul traffic is arriving on time. For this run: 

    .. code-block:: bash
    
      tail -f /var/log/rrh_log_print/rrh_log_print.log  | grep xRN

  The RU should be printing something like the following every second: 

    .. code-block:: bash
    
      [2024-05-10 08:28:23.034] xRN: total=2740860 c_early=0 c_on=218300 c_late=0 err_tci=0 err_ecpri=0 err_port=0 err_sct=0 err_total=1443194
  
  Verify that the the values in the ``c_on`` column and the ``err_total`` column increase but all other columns should be zero. Note the misleading name, in the ``err_total`` column 
  the RU actually counts for uplane packets as well. This has been fixed in later firmware releases.

Connecting to the network
=========================

You can now connect a UE to the network. This can be done using e.g. a COTS UE. See the main RU guide for details on this.