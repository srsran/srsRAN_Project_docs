.. _manual_config_ref: 

Configuration Reference
#######################

The srsRAN Project gNB uses a yaml (.yml) configuration file. This file can be created and customized by users as needed, and comes with a vast array of configuration options to suit all use-cases. 

Example Config Files
********************

The srsRAN Project gNB comes with example configuration files, these can be found in ``srsRAN_Project/configs/`` in the source code. 

You can also download these sample gNB configuration files here:  

    - `B200 USRP @ 20 MHz in band 78 (TDD) <https://github.com/srsran/srsRAN_Project/blob/main/configs/gnb_rf_b200_tdd_n78_10mhz.yml>`_
    - `N310 USRP @ 20 MHz in band 3 (FDD) <https://github.com/srsran/srsRAN_Project/blob/main/configs/gnb_rf_n310_fdd_n3_20mhz.yml>`_

These configuration file examples provide a basic set-up to get users up and running, users can easily modify these to suit their use-case. Each config file contains comments explaining the parameters being configured. 
Both of these configuration files ship as standard with the srsRAN Project codebase, they can be found in the configs folder. 

----

Running with a Config File
**************************

As mentioned above, the gNB takes a yaml type configuration file (.yml). From here users can easily configure each of the available parameters of the gNB.

To run the gNB with a config file, the following command can be used: 

.. code-block:: bash

   sudo ./gnb -c [PATH TO FILE]


To see the full list of options that can be configured, use following command: 

.. code-block:: bash

   ./gnb --help

-----

Configuration Options
*********************

gnb_id
  - Optional UINT, expected value is an integer (Default is 411). Sets the numerical ID associated with the gNB. 

ran_node_name
  - Optional TEXT, expected value is a single text string with no spaces (Default is srsgnb01). Sets the text ID associated with the gNB. 

amf
=======

  addr
    - Required TEXT, expected value is an IPV4 or IPV6 IP address (no default, must be set by the user). This sets the IP address or hostname of the AMF.

  port
    - Optional UINT, expected value between [20000 - 40000] (default is 38412). This assigns the AMF port. 

  bind_addr
    - Required TEXT, expected value is an IPV4 or IPV6 IP address (no default, must be set by the user). This sets the local IP address that the gNB binds to for receiving traffic from the AMF. 

rf_driver
=============

  srate
    - Required FLOAT, expected value is sampling rate within the capabilities of your frontend(default is 61.44 Mhz). Sets the sampling rate of the RF-frontend in MHz. 

  device_driver
    - Required TEXT, expected value is name of driver being used [e.g. zmq, uhd, ...](default is uhd). Device driver name. 

  device_args
    - Optional TEXT, expected value is a string accepted by the RF driver. This will be an argument that gets passed to the selected RF driver.  

  tx_gain
    - Required FLOAT, expected value between [0 - max value supported by frontend](default is 50). This sets the transmit gain in dB.  

  rx_gain
    - Required FLOAT, expected value between [0 - max value supported by frontend](default is 60). This sets the receive gain in dB.

  lo_offset
    - Optional FLOAT, expected value is any positive or negative value (default is 0). It shifts the LO from the center frequency for moving the LO leakage out of the channel

  clock
    - Optional TEXT, expected values DEFAULT, INTERNAL, EXTERNAL, GPSDO (default is to use the RF-frontend's onboard clock). Setting this will select the source where the RF-frontend gets its clock source.

  sync
    - Optional TEXT, expected values DEFAULT, INTERNAL, EXTERNAL, GPSDO (default is to use the RF-frontend's onboard clock). This will select the time synchronization source. 

  time_alignment_calibration
    - Optional UINT, expected value is any positive or negative integer (default is 0). This compensates for the reception and transmission time misalignment inherent to the RF device. Positive values reduce the RF transmission delay with respect to the RF reception. Negative values have the opposite effect.

cell_cfg
============

  pci
    - Required UINT, expected value between [0 - 1007] (Default is 1). Sets the Physical Cell ID. 

  dl_arfcn
    - Required UINT, expected value for valid ARFCN code within the working range of your frontend(Default is 536020). Sets the Downlink ARFCN. It is recommended to find an ARFCN which is not in licensed spectrum. 

  band
    - Required TEXT, expected value must be a valid NR band for your given cell configuration and be supported by the gNB implementation (Default will automatically set band based on ARFCN). Sets the NR band being used for the cell.
    - Current unsupported bands are:

      - All SCS: n78
      - 15 kHz SCS: n34, n38, n39

  common_scs
    - Required ENUM, expected value is either 15 or 30 kHz (Default is 15 kHz). Sets the subcarrier spacing to be used by the cell. 

  channel_bandwidth_MHz
    - Required ENUM, expected value is one of the following [5,10,15,20,25,30,40,50,60,70,80,90,100] (Default is 20). Sets the channel Bandwidth in MHz, the number of PRBs will be derived from this. 

  nof_antennas_ul
    - Optional UINT, expected value is 1 (Default is 1). Sets number of antenna for downlink transmission. Currently only a single antenna is supported.  

  nof_antennas_dl
    - Optional UINT, expected value is 1 (Default is 1). Sets number of antenna for uplink transmission. Currently only a single antenna is supported. 

  plmn
    - Required TEXT, expected value is 7-digit PLMN code containing MCC & MNC (Default is 00101). This sets the Public Land Mobile Network code. 

  tac
    - Required UINT, expected value is a non-zero positive integer value (Default is 7). This sets the Tracking Area Code. 

  pdsch
    - Further optional subcommands that allow the configuration of the Physical Downlink Shared Channel of the cell. Configurable options include the Modulation and Coding Schemes used by the UE, Random Access Response, and System Information Block 1. srsRAN Project currently only supports MCS values from `MCS Table 1 <https://www.sharetechnote.com/html/5G/5G_MCS_TBS_CodeRate.html#:~:text=%3C%2038.214%20%C2%A0%2D%20Table%205.1.3.1%2D1%3A%20MCS%20index%20table%201%20for%20PDSCH%C2%A0%3E>`_ for all configurable MCS values.

      - **fixed_ue_mcs**: Optional INT, expected value is a valid MCS index integer value [0 - 28] (Default is dynamic). Sets a fixed MCS value to be used by the gNB when communicating with the UE. If this value is not set then it will be set automatically based on the channel conditions.  
      - **fixed_rar_mcs**: Optional INT, expected value is a valid MCS index with modulation order 2 in the range [0 - 9] from MCS Table 1 (Default is 0). Sets a fixed MCS value to be used when sending the RAR from the gNB to the UE. 
      - **fixed_sib1_mcs**:  Optional INT, expected value is a valid MCS index with modulation order 2 in the range [0 - 9] from MCS Table 1 (Default is 5). Sets a fixed MCS to be used when sending the SIB1 from the gNB to the UE. 

  pusch
    - Further optional subcommand that allows the configuration of the Physical Uplink Shared Channel of the cell. Configurable options include the Modulation and Coding Schemes used by the UE. Currently srsRAN Project only supports values from Table 1 (as stated above).

      - **fixed_ue_mcs**: Optional INT, expected value is a valid MCS index integer value [0 - 28] (Default is dynamic). Sets a fixed MCS value to be used by the UE when communicating with the UE. If this value is not set then it will be set automatically based on the channel conditions. 

  prach
    - Further optional subcommands that allow the configuration of the Physical Random Access Channel of the cell. Configurable options include the configuration index, root sequence index, zero correlation zone index, the message 3 MCS and the maximum number of message 3 HARQ retransmissions. 

      - **prach_config_index** : Optional INT, expected value is an integer in the range [0 - 255] based on the PRACH configuration index table for FR1 (Default is 1). Sets the PRACH configuration index, which determines the format and content of the PRACH preamble. You find the relevant table `here <https://www.sharetechnote.com/html/5G/5G_RACH.html#Preamble_Format_0:~:text=%3C%2038.211%20v15.5.0%2DTable%206.3.3.2%2D2%3A%20Random%20access%20configurations%20for%20FR1%20and%20paired%20spectrum/supplementary%20uplink%C2%A0%3E>`_.
      - **prach_root_sequence_index** : Optional INT, expected value is an integer in the range [0 - 837] (Default is 1). Sets the PRACH Roost Sequence Index (RSI), which determines the Zadoff-Chu (ZC) sequence used. If the PRACH configuration index is larger than 86, you cannot set a PRACH RSI of more than 137. 
      - **zero_correlation_zone** : Optional INT, expected value is an integer in the range [0 - 15] (Default is 0). Sets the Zero Correlation Zone, which determines the size of the cyclic shift and the number of preamble sequences which can be generated from each Root Sequence Index. 
      - **fixed_msg3_mcs** : Optional INT, expected value is an integer in the range [0 - 28] (Default is 0). Sets a fixed message 3 MCS. 
      - **max_msg3_harq_retx** : Optional INT, expected value is an integer in the range [0 - 4] (Default is 4). Sets the maximum number of message 3 Hybrid Automatic Repeat Request (HARQ) retransmissions. 

  amplitude_control
    - Further optional subcommands that allow the configuration of the amplitude control of the physical signal transmitted by the cell. Configurable options include the TX gain back-off, signal clipping and the clipping ceiling. 

      - **tx_gain_backoff** : Optional FLOAT, expected value is a positive value or 0 (Default is 12.0 dB). Sets baseband gain back-off in dB. This accounts for the signal Peak-to-Average Power Ratio (PAPR) and is applied regardless of clipping settings.
      - **enable_clipping** : Optional BOOL, expected value is true or false (default is false). Sets clipping of the baseband samples on or off. If enabled, the samples that exceed the power ceiling are clipped.
      - **ceiling** : Optional FLOAT, expected value is a negative value or 0 (Default is 0 dB). Sets the power ceiling in dB, relative to the full scale amplitude of the radio.

log
=======

  All log levels can be configured independently to output at various levels of detail. Logs can be configured to the following levels (from lowest to highest levels of detail): 

    - none
    - error 
    - warning 
    - info
    - debug

  filename
    - Optional TEXT, expected value is file path and name of file for logs to be printed to (Default is /tmp/gnb.log).

  all_level
    - Optional TEXT, expected value is one of the above log level indicators (Default is warning). Sets log level across PHY, MAC, RLC, PDCP, RRC, SDAP, NGAP and GTPU. 

  phy_level
    - Optional TEXT, expected value is one of the above log level indicators (Default is warning). Sets PHY log level. 

  mac_level
    - Optional TEXT, expected value is one of the above log level indicators (Default is warning). Sets MAC log level. 

  rlc_level
    - Optional TEXT, expected value is one of the above log level indicators (Default is warning). Sets RLC log level. 

  pdcp_level
    - Optional TEXT, expected value is one of the above log level indicators (Default is warning). Sets PDCP log level. 

  rrc_level
    - Optional TEXT, expected value is one of the above log level indicators (Default is warning). Sets RRC log level. 

  sdap_level
    - Optional TEXT, expected value is one of the above log level indicators (Default is warning). Sets SDAP log level.

  ngap_level
    - Optional TEXT, expected value is one of the above log level indicators (Default is warning). Sets NGAP log level.

  gtpu_level
    - Optional TEXT, expected value is one of the above log level indicators (Default is warning). Sets GTPU log level.

  radio_level
    - Optional TEXT, expected value is one of the above log level indicators (Default is warning). Sets radio log level.

  fapi_level
    - Optional TEXT, expected value is one of the above log level indicators (Default is warning). Sets FAPI log level.

  f1u_level
    - Optional TEXT, expected value is one of the above log level indicators (Default is warning). Sets F1u log level.

  du_level
    - Optional TEXT, expected value is one of the above log level indicators (Default is warning). Sets DU log level.

  cu_level
    - Optional TEXT, expected value is one of the above log level indicators (Default is warning). Sets CU log level.

  lib_level
    - Optional TEXT, expected value is one of the above log level indicators (Default is warning). Sets generic log level.

  hex_max_size
    - Optional INT, expected value is in the range [0 - 1024] (Default is 0). Sets maximum number of bytes to print in hex (zero for no hex dumps)

  broadcast_enabled
    - Optional BOOL, expected value is true or false (Default is false). Enables logging in the physical and MAC layer of broadcast messages and all PRACH opportunities. 

  phy_rx_symbols_filename
    - Optional TEXT, expected value is file name and path (Default is not set, meaning no received symbols will be printed). Set to a valid file path to print the received symbols.

pcap
========

  ngap_filename
    - Optional TEXT, expected value is file path and name of file for NGAP PCAPs to be printed to (Default is /tmp/gnb_ngap.pcap). 

  ngap_enable
    - Optional BOOL, expected value is true or false (default is false). Enables NGAP packet capture.

  mac_filename
    - Optional TEXT, expected value is file path and name of file for MAC PCAPs to be printed to (Default is /tmp/gnb_mac.pcap). 

  mac_enable
    - Optional BOOL, expected value is true or false (default is false). Enables MAC packet capture.

expert_phy
==============

  nof_ul_threads
    - Optional UINT, expected value is a non-zero integer and is bound by the limitations of the PC (Default is 4). Sets number of threads for processing PUSCH and PUCCH. It is set to 4 by default unless the available hardware concurrency is limited in which case will use a minimum of one thread.

  pusch_dec_max_iterations
    - Optional UINT, expected value must be a positive non-zero integer (Default is 6). Sets the number of PUSCH LDPC decoder iterations. 

  pusch_dec_enable_early_stop
    - Optional BOOL, expected value is true or false (Default is true). Enables the PUSCH decoder early stop. 

