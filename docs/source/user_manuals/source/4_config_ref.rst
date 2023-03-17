.. _manual_config_ref: 

Configuration Reference
#######################

The srsRAN Project gNB application uses a YAML (.yml) configuration file. 

The gNB comes with a number of example configuration files, these can be found in ``srsRAN_Project/configs/`` in the source code: 

    - `B200 USRP @ 20 MHz in band 78 (TDD) <https://github.com/srsran/srsRAN_Project/blob/main/configs/gnb_rf_b200_tdd_n78_10mhz.yml>`_
    - `N310 USRP @ 20 MHz in band 3 (FDD) <https://github.com/srsran/srsRAN_Project/blob/main/configs/gnb_rf_n310_fdd_n3_20mhz.yml>`_

These configuration file examples provide a basic set-up to get users up and running, users can easily modify these to suit their use-case.  

----

Format
******

All configuration parameters are presented here below in the following format:

*parameter*
  - Optional/Required *TYPE* (*default*). *Description*. Format: *format description*. Supported: *supported values*.

----

Configuration Parameters
************************


gnb_id
  - Optional UINT (411). Sets the numerical ID associated with the gNB.

ran_node_name
  - Optional TEXT (srsgnb01). Sets the text ID associated with the gNB. Format: string without spaces.

amf
=======

  addr
    - Required TEXT. Sets the IP address or hostname of the AMF. Format: IPV4 or IPV6 IP address.

  port
    - Optional UINT (38412). Sets the AMF port. Format: integer between [20000 - 40000].

  bind_addr
    - Required TEXT. Sets the local IP address that the gNB binds to for receiving traffic from the AMF. Format: IPV4 or IPV6 IP address.

rf_driver
=============

  srate
    - Required FLOAT (61.44). Sets the sampling rate of the RF-frontend in MHz. 

  device_driver
    - Required TEXT (uhd). RF device driver name. Supported: [uhd].

  device_args
    - Optional TEXT. An argument that gets passed to the selected RF driver.  

  tx_gain
    - Required FLOAT (50). Sets the transmit gain in dB. Supported: [0 - max value supported by radio].

  rx_gain
    - Required FLOAT (60). Sets the receive gain in dB. Supported: [0 - max value supported by radio].

  lo_offset
    - Optional FLOAT (0). Shifts the local oscillator frequency in MHz away from the center frequency to move LO leakage out of the channel.

  clock
    - Optional TEXT (default). Specify the RF device source for timestamping. Supported: [default, internal, external, gpsdo].

  sync
    - Optional TEXT (default). Specify the RF device oscillator reference synchronization source. Supported: [default, internal, external, gpsdo].

  time_alignment_calibration
    - Optional UINT (0). Compensates for any reception and transmission time misalignment inherent to the RF device. Positive values reduce the RF transmission delay with respect to the RF reception. Negative values have the opposite effect.

cell_cfg
============

  pci
    - Required UINT (1). Sets the Physical Cell ID. Supported: [0-1007].

  dl_arfcn
    - Required UINT (536020). Sets the Downlink ARFCN. 

  band
    - Optional UINT. Sets the NR band being used for the cell. If not specified, will be set automatically based on ARFCN.
    - Current unsupported bands are:

      - All SCS: 79
      - 15 kHz SCS: 34, 38, 39

  common_scs
    - Required UINT (15). Sets the subcarrier spacing in KHz to be used by the cell. Supported: [15, 30].

  channel_bandwidth_MHz
    - Required UINT (20). Sets the channel Bandwidth in MHz, the number of PRBs will be derived from this. Supported: [5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100].

  nof_antennas_ul
    - Optional UINT (1). Sets the number of antennas for downlink transmission. Supported: [1].

  nof_antennas_dl
    - Optional UINT (1). Sets the number of antennas for uplink transmission. Supported: [1].

  plmn
    - Required TEXT (00101). Sets the Public Land Mobile Network code. Format: 7-digit PLMN code containing MCC & MNC.

  tac
    - Required UINT (7). Sets the Tracking Area Code. 

  pdsch
    - Further optional parameters to configure the Physical Downlink Shared Channel of the cell. 

      - **fixed_ue_mcs**: Optional UINT. Sets a fixed PDSCH MCS value to be used for all UEs. Supported: [0 - 28].  
      - **fixed_rar_mcs**: Optional UINT (0). Sets a fixed RAR MCS value for all UEs. Supported: [0 - 9].
      - **fixed_sib1_mcs**:  Optional UINT (5). Sets a fixed SIB1 MCS for all UEs. Supported: [0 - 9].

  pusch
    - Further optional parameters to configure the Physical Uplink Shared Channel of the cell.

      - **fixed_ue_mcs**: Optional UINT. Sets a fixed PUSCH MCS for all UEs. Supported: [0 - 28].

  prach
    - Further optional parameters to configure the Physical Random Access Channel of the cell. 

      - **prach_config_index** : Optional UINT (1). Sets the PRACH configuration index. Supported: [0 - 255]. 
      - **prach_root_sequence_index** : Optional UINT (1). Sets the PRACH Roost Sequence Index (RSI), which determines the Zadoff-Chu (ZC) sequence used. Supported: [0 - 837]. If the PRACH configuration index is larger than 86, you cannot set a PRACH RSI of more than 137. 
      - **zero_correlation_zone** : Optional UINT (0). Sets the Zero Correlation Zone, which determines the size of the cyclic shift and the number of preamble sequences which can be generated from each Root Sequence Index. Supported: [0 - 15]. 
      - **fixed_msg3_mcs** : Optional UINT (0). Sets a fixed Msg3 MCS. Supported: [0 - 28].  
      - **max_msg3_harq_retx** : Optional UINT (4). Sets the maximum number of Msg3 HARQ retransmissions. Supported: [0 - 4]. 

  amplitude_control
    - Further optional parameters to configure the amplitude control of the physical signal transmitted by the cell. 

      - **tx_gain_backoff** : Optional FLOAT (12.0). Sets baseband gain back-off in dB. This accounts for the signal Peak-to-Average Power Ratio (PAPR) and is applied regardless of clipping settings. Format: positive float. 
      - **enable_clipping** : Optional BOOL (false). Sets clipping of the baseband samples on or off. If enabled, samples that exceed the power ceiling are clipped.
      - **ceiling** : Optional FLOAT (0.0). Sets the power ceiling in dB, relative to the full scale amplitude of the radio. Format: negative float or 0.

log
=======

  All gNB layers and components can be configured independently to output at various levels of detail. Logs can be configured to the following levels (from lowest to highest levels of detail): 

    - none
    - error 
    - warning 
    - info
    - debug

  filename
    - Optional TEXT (/tmp/gnb.log). File path for logs.

  all_level
    - Optional TEXT (warning). Sets a common log level across PHY, MAC, RLC, PDCP, RRC, SDAP, NGAP and GTPU layers. 

  phy_level
    - Optional TEXT (warning). Sets PHY log level. 

  mac_level
    - Optional TEXT (warning). Sets MAC log level. 

  rlc_level
    - Optional TEXT (warning). Sets RLC log level. 

  pdcp_level
    - Optional TEXT (warning). Sets PDCP log level. 

  rrc_level
    - Optional TEXT (warning). Sets RRC log level. 

  sdap_level
    - Optional TEXT (warning). Sets SDAP log level.

  ngap_level
    - Optional TEXT (warning). Sets NGAP log level.

  gtpu_level
    - Optional TEXT (warning). Sets GTPU log level.

  radio_level
    - Optional TEXT (warning). Sets radio log level.

  fapi_level
    - Optional TEXT (warning). Sets FAPI log level.

  f1u_level
    - Optional TEXT (warning). Sets F1u log level.

  du_level
    - Optional TEXT (warning). Sets DU log level.

  cu_level
    - Optional TEXT (warning). Sets CU log level.

  lib_level
    - Optional TEXT (warning). Sets generic log level.

  hex_max_size
    - Optional UINT (0). Sets maximum number of bytes to print for hex messages. Supported: [0 - 1024]. 

  broadcast_enabled
    - Optional BOOL (false). Enables logging in the PHY and MAC layer of broadcast messages and all PRACH opportunities. 

  phy_rx_symbols_filename
    - Optional TEXT. Print received symbols to file. Symbols will be printed if a valid path is set. Format: file path.

pcap
========

  ngap_enable
    - Optional BOOL (false). Enable/disable NGAP packet capture.
    
  ngap_filename
    - Optional TEXT (/tmp/gnb_ngap.pcap). Path for NGAP PCAPs. 

  mac_enable
    - Optional BOOL (false). Enable/disable MAC packet capture.
    
  mac_filename
    - Optional TEXT (/tmp/gnb_mac.pcap). Path for MAC PCAPs.



expert_phy
==============

  nof_ul_threads
    - Optional UINT (4). Sets number of threads for processing PUSCH and PUCCH. It is set to 4 by default unless the available hardware concurrency is limited in which case will use a minimum of one thread.

  pusch_dec_max_iterations
    - Optional UINT (6). Sets the number of PUSCH LDPC decoder iterations. Format: Positive integer greater than 0.

  pusch_dec_enable_early_stop
    - Optional BOOL (true). Enables the PUSCH decoder early stopping mechanism. 

