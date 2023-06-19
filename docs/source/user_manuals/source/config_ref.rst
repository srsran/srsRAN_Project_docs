.. _manual_config_ref:

Configuration Reference
#######################

The srsRAN Project gNB application uses a YAML (.yml) configuration file.

The gNB comes with a number of example configuration files, these can be found in ``srsRAN_Project/configs/`` in the source code:

    - `B200 USRP @ 20 MHz in band 78 (TDD) <https://github.com/srsran/srsRAN_Project/blob/main/configs/gnb_rf_b200_tdd_n78_20mhz.yml>`_
    - `N310 USRP @ 20 MHz in band 3 (FDD) <https://github.com/srsran/srsRAN_Project/blob/main/configs/gnb_rf_n310_fdd_n3_20mhz.yml>`_

These configuration file examples provide a basic set-up to get users up and running, users can easily modify these to suit their use-case.

More example configuration files for various use cases can be found `here <https://github.com/srsran/srsRAN_Project/tree/main/configs>`_.

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

gnb_id_bit_length
  - Optional UNIT. Sets the bit length of the gnb_id above. Format: integer between [22 - 32]

ran_node_name
  - Optional TEXT (srsgnb01). Sets the text ID associated with the gNB. Format: string without spaces.

cells
  - Optional TEXT. Sets the cell configuration on a per cell basis, overwriting the default configuration defined by ``cell_cfg``. Contains a list of cells, each with parameters that overwrite the default config. This can only be set via the configuration file. For more information see the relevant example configuration file `gnb_custom_cell_properties.yml <https://github.com/srsran/srsRAN_Project/tree/main/configs>`_.

.. note::
  Currently only single cell configuration is support, multi-cell support is expected to be added in the coming months.

qos
  - Optional TEXT. Configures RLC and PDCP radio bearers on a per 5QI basis. This can only be set via the configuration file.

slicing
  - Optional TEXT. Configure network slicing options. This can only be set via the configuration file. May contain the following parameters: 

    - **sst**: Optional UINT (1). Sets the Slice Service Type. Supported: [0 - 255].
    - **sd**: Optional UINT (0). Sets the Service Differentiator. Supported: [0-16777215].

amf
=======

  addr
    - Required TEXT. Sets the IP address or hostname of the AMF. Format: IPV4 or IPV6 IP address.

  port
    - Optional UINT (38412). Sets the AMF port. Format: integer between [20000 - 40000].

  bind_addr
    - Required TEXT. Sets the local IP address that the gNB binds to for receiving traffic from the AMF. Format: IPV4 or IPV6 IP address.

  sctp_rto_initial
    - Optional INT. Sets the initial retransmission timeout when creating the SCTP connection.

  sctp_rto_min
    - Optional INT. Sets the minimum retransmission timeout for the SCTP connection.

  sctp_rto_max
    - Optional INT. Sets the maximum retransmission timeout for the SCTP connection.

  sctp_initial_max_attempts 
    - Optional INT. Sets the maximum retransmission attempts for the initial SCTP connection.

  sctp_initial_max_timeo 
    - Optional INT. Sets the maximum retransmission timeout for the initial SCTP connection.

  no_core
    - Optional BOOLEAN (0). Setting to true allows the gNB to run without a core. Supported: [0, 1]. 

cu_cp
=====

  inactivity_timer
    - Optional INT (72000). Sets the UE/PDU Session/DRB inactivity timer in seconds. Supported: [1 - 7200].

ru_sdr
=============

This section of the configuration file should be used when connecting the srsRAN Project gNB to a USRP using split 8 interface.

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

  freq_offset
    - Optional FLOAT (0). Sets the frequency offset in Hertz.

  clock_ppm
    - Optional FLOAT (0). Sets the clock calibration in Parts Per Million (PPM).

  lo_offset
    - Optional FLOAT (0). Shifts the local oscillator frequency in MHz away from the center frequency to move LO leakage out of the channel.

  clock
    - Optional TEXT (default). Specify the RF device source for timestamping. Supported: [default, internal, external, gpsdo].

  sync
    - Optional TEXT (default). Specify the RF device oscillator reference synchronization source. Supported: [default, internal, external, gpsdo].

  otw_format
    - Optional TEXT (default). Specific the over-the-wire format. Supported: [default, sc8, sc12, sc16].

  time_alignment_calibration
    - Optional UINT (0). Compensates for any reception and transmission time misalignment inherent to the RF device. Positive values reduce the RF transmission delay with respect to the RF reception. Negative values have the opposite effect.

  cells
    - Optional TEXT. Sets the hardware specific cell configuration on a per cell basis. May contain the following parameters:

      - **amplitude_control**

        - **tx_gain_backoff**: Optional FLOAT (12.0). Sets baseband gain back-off in dB. This accounts for the signal PAPR and is applied regardless of clipping settings. Format: positive float.
        - **enable_clipping**: Optional BOOL (false). Sets clipping of the baseband samples on or off. If enabled, samples that exceed the power ceiling are clipped.
        - **power_ceiling_dBFs**: Optional FLOAT (-0.1). Sets the power ceiling in dB, relative to the full scale amplitude of the radio. Format: negative float or 0.

  expert_cfg
    - Further optional parameters to configure RF-frontend.

      - **low_phy_thread_profile**: Optional TEXT. Lower physical layer executor profile. Supported: [single, dual, quad].

ru_ofh
======

This section of the configuration file should be used when connecting the srsRAN Project gNB to an O-RAN RU using split 7.2 interface.

.. note::

  Many of the following values are optional as they have default values. In practice, all of the following parameters should be defined by the user, as they will need
  to be configured specifically for the RU being used. Failing to configure this parameters correctly may result in the RU failing to connect correctly to the DU.
\

  max_proc_delay
    - Optional UINT (2). Sets the maximum allowed processing delay in slots. Supported: [1 - 30].

  gps_alpha
    - Optional FLOAT (0). Sets the GPS alpha. Supported: [0 - 1.2288e+07].

  gps_beta
    - Optional INT (0). Sets the GPS beta. Supported: [-32768 - +32767]. 

  ru_bandwidth_MHz
    - Required UINT (0). Sets the channel bandwidth in MHz. Supported: [5,10,15,20,25,30,40,50,60,70,80,90,100].

  t1a_max_cp_dl
    - Optional INT (500). Sets T1a maximum value for downlink control-plane. Supported: [0 - 1960].

  t1a_min_cp_dl
    - Optional INT (258). Sets T1a minimum value for downlink control-plane. Supported: [0 - 1960].

  t1a_max_cp_ul
    - Optional INT (500). Sets T1a maximum value for uplink control-plane. Supported: [0 - 1960].

  t1a_min_cp_ul
    - Optional INT (258). Sets T1a minimum value for uplink control-plane. Supported: [0 - 1960].

  t1a_max_up
    - Optional INT (300).Sets T1a maximum value for uer-plane. Supported: [0 - 1960].

  t1a_min_up
    - Optional INT (85). Sets T1a minimum value for user-plane. Supported: [0 - 1960].

  is_prach_cp_enabled
    - Optional BOOLEAN (0). Sets PRACH control-plane enabled flag. Supported: [0, 1].

  is_dl_broadcast_enabled
    - Optional BOOLEAN (0). Sets downlink broadcast enabled flag. Supported: [0, 1].

  compr_method_ul
    - Optional TEXT (bfp). Sets the uplink compression method. Supported: [none, bfp, bfp selective, block scaling, mu law, modulation, modulation selective].

  compr_bitwidth_ul
    - Optional UINT (9). Sets the uplink compression bit width. Supported: [1 - 16].

  compr_method_dl
    - Optional TEXT (bfp). Sets the downlink compression method. Supported: [none, bfp, bfp selective, block scaling, mu law, modulation, modulation selective].

  compr_bitwidth_dl
    - Optional UINT (9). Sets the downlink compression bit width. Supported: [1 - 16].

  iq_scaling
    - Optional FLOAT (0.35). Sets the IQ scaling factor. Supported: [0 - 1].

  cells
    - Optional TEXT. Sets the hardware specific cell configuration on a per cell basis. May contain the following parameters:

      - **network_interface**: Optional TEXT ("enp1s0f0"). Sets the ethernet network interface name for the RU. Format: a string, e.g. ["interface_name"].
      - **ru_mac_address**: Optional TEXT ("70:b3:d5:e1:5b:06"). Sets the RU MAC address. Format: a string, e.g. ["AA:BB:CC:DD:11:22:33"].
      - **du_mac_address**: Optional TEXT ("00:11:22:33:00:77"). Sets the DU MAC address. Format: a string, e.g. ["AA:BB:CC:DD:11:22:33"].
      - **vlan_tag**: Optional UINT (1). Sets the V-LAN tag control information field. Supported: [1 - 4094].
      - **ru_prach_port_id**: Optional UINT (4). Sets the RU PRACH eAxC port ID. Supported: [0 - 65535].
      - **ru_dl_port_id**: Optional UINT (0, 1). Sets the RU downlink eAxC port ID. Format: vector containing all DL eXaC ports, e.g. [0, ...\ , N].
      - **ru_ul_port_id**: Optional UINT (0). Sets the RU uplink eAxC port ID. Supported: [0 - 65535].

cell_cfg
========

This is the default configuration that will be inherited by all cells, overwritten in the ``cells`` list.

  pci
    - Required UINT (1). Sets the Physical Cell ID. Supported: [0-1007].

  dl_arfcn
    - Required UINT (536020). Sets the Downlink ARFCN.

  band
    - Optional UINT. Sets the NR band being used for the cell. If not specified, will be set automatically based on ARFCN. Supported: all release 17 bands.

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

  q_rx_lev_min
    - Optional INT (-70). Sets the required minimum received RSRP level for cell selection/re-selection, in dBm. Supported: [-70 - -22]. 
  
  q_qual_min
    - Optional INT (-20). Sets the required minimum received RSRQ level for cell selection/re-selection, in dB. Supported: [-43 - -12].

  pcg_p_nr_fr1
    - Optional INT (10). Sets the maximum total TX power to be used by the UE in this NR cell group across in FR1. Supported: [-30 - +33]. 

  ssb 
    - Further optional parameters to configure the Synchronization Signal Block of the cell. 
    
      - **ssb_period**: Optional UINT (10). Sets the period of SSB scheduling in milliseconds. Supported: [5, 10, 20]. 
      - **ssb_block_power_dbm**: Optional INT (-16). Sets the SS PBCH block power in dBm. Supported: [-60 - +50]. 
      - **pss_to_sss_epre_db**: Optional UINT (0). Sets the Synchronization Signal Block Primary Synchronization Signal to Secondary Synchronization Signal Energy Per Resource Element ratio in dB. Supported: [0, 3].

  pdcch
    - Further optional parameters to configure the Physical Downlink Control Channel of the cell. 
  
      - **ss_type**: Optional TEXT (ue_dedicated). Sets the Search Space type for the UE data. Supported: [common, ue_dedicated].  
      - **dci_format_0_1_and_1_1**: Optional BOOLEAN (1). Sets whether to use non-fallback or fallback DCI format in UE dedicated SearchSpace. Supported: [0, 1]. 


  pdsch
    - Further optional parameters to configure the Physical Downlink Shared Channel of the cell.

      - **min_ue_mcs**: Optional UINT. Sets a minimum PDSCH MCS value to be used for all UEs. Supported: [0 - 28].
      - **max_ue_mcs**: Optional UINT. Sets a maximum PDSCH MCS value to be used for all UEs. Supported: [0 - 28].
      - **fixed_rar_mcs**: Optional UINT (0). Sets a fixed RAR MCS value for all UEs. Supported: [0 - 9].
      - **fixed_sib1_mcs**:  Optional UINT (5). Sets a fixed SIB1 MCS for all UEs. Supported: [0 - 9].
      - **nof_harqs**: Optional UNIT (16). Sets the number of Downlink HARQ processes. Supported [2, 4, 6, 8, 10, 12, 16]
      - **max_consecutive_kos**: Optional UINT (100). Sets the maximum number of consecutive HARQ-ACK KOs before an RLF is reported. Supported: [0 - inf]
      - **rv_sequence**: Optional UINT (0,2,3,1). Sets the redundancy version sequence to use for PDSCH. Supported: any combination of [0, 1, 2, 3]. 
      - **mcs_table**: Optional TEXT (qam64). Sets the MCS table to use for PDSCH. Supported: [qam64, qam256]. 
      - **nof_ports**: Optional TEXT. Sets the number of ports for PDSCH. By default it is set to be equal to number of DL antennas Supported: [1,2].

  pusch
    - Further optional parameters to configure the Physical Uplink Shared Channel of the cell.

      - **min_ue_mcs**: Optional UINT. Sets a minimum PUSCH MCS value to be used for all UEs. Supported: [0 - 28].
      - **max_ue_mcs**: Optional UINT. Sets a maximum PUSCH MCS value to be used for all UEs. Supported: [0 - 28].
      - **max_consecutive_kos**: Optional UINT (100). Sets the maximum number of consecutive CRC KOs before an RLF is reported. Supported: [0 - inf]
      - **rv_sequence**: Optional UINT (0). Sets the redundancy version sequence to use for PUSCH. Supported: any combination of [0, 1, 2, 3]. 
      - **mcs_table**: Optional TEXT (qam64). Sets the MCS table to use for PDSCH. Supported: [qam64, qam256]. 
      - **msg3_delta_preamble**: Optional INT (6). Sets the MSG3 DeltaPreamble power offset between MS3 and RACH preamble transmission. Supported: [-1 - 6]. 
      - **p0_nominal_with_grant**: Optional INT (-76). Sets the P0 value for PUSCH grant (except MSG3), in dBm. Supported: multiples of 2 within the range [-202, 24]. 
      - **msg3_delta_power**: Optional INT (8). Sets the target power level at the network receiver side, in dBm. Supported: multiples of 2 within the range [-6, 8]. 
      - **b_offset_ack_idx_1**: Optional UINT (9). Sets the betaOffsetACK-Index1 part of UCI-OnPUSCH. Supported: [0 - 31].
      - **b_offset_ack_idx_2**: Optional UINT (9). Sets the betaOffsetACK-Index2 part of UCI-OnPUSCH. Supported: [0 - 31].
      - **b_offset_ack_idx_3**: Optional UINT (9). Sets the betaOffsetACK-Index3 part of UCI-OnPUSCH. Supported: [0 - 31].
      - **beta_offset_csi_p1_idx_1**: Optional UINT (9). Sets the b_offset_csi_p1_idx_1 part of UCI-OnPUSCH. Supported: [0 - 31].
      - **beta_offset_csi_p1_idx_2**: Optional UINT (9). Sets the b_offset_csi_p1_idx_2 part of UCI-OnPUSCH. Supported: [0 - 31].
      - **beta_offset_csi_p2_idx_1**: Optional UINT (9). Sets the b_offset_csi_p2_idx_1 part of UCI-OnPUSCH. Supported: [0 - 31].
      - **beta_offset_csi_p2_idx_2**: Optional UINT (9). Sets the b_offset_csi_p2_idx_2 part of UCI-OnPUSCH. Supported: [0 - 31].

  prach
    - Further optional parameters to configure the Physical Random Access Channel of the cell.

      - **prach_config_index**: Optional UINT (1). Sets the PRACH configuration index. Supported: [0 - 255].
      - **prach_root_sequence_index**: Optional UINT (1). Sets the PRACH Roost Sequence Index (RSI), which determines the Zadoff-Chu (ZC) sequence used. Supported: [0 - 837]. If the PRACH configuration index is larger than 86, you cannot set a PRACH RSI of more than 137.
      - **zero_correlation_zone**: Optional UINT (0). Sets the Zero Correlation Zone, which determines the size of the cyclic shift and the number of preamble sequences which can be generated from each Root Sequence Index. Supported: [0 - 15].
      - **fixed_msg3_mcs**: Optional UINT (0). Sets a fixed Msg3 MCS. Supported: [0 - 28].
      - **max_msg3_harq_retx**: Optional UINT (4). Sets the maximum number of Msg3 HARQ retransmissions. Supported: [0 - 4].
      - **total_nof_ra_preambles**: Optional TEXT. Sets the number of different PRACH preambles. Supported: [1 - 64].
      - **prach_frequency_start**: Optional INT. Set Offset of lowest PRACH transmission occasion in frequency domain respective to PRB 0, in PRBs. Supported: [0 - (MAX_NOF_PRB - 1)].
      - **preamble_rx_target_pw**: Optional INT (-100). Sets the Target power level at the network receiver side, in dBm. Supported: multiples of 2 within range [-202, -60]. 

  tdd_ul_dl_cfg
    - Further optional parameters to configure the TDD Uplink and Downlink configuration parameters.

      - **dl_ul_tx_period**: Optional FLOAT (5). TDD pattern periodicity in milliseconds. Supported: [0 - 10].
      - **nof_dl_slots**: Optional INT (6). Number of consecutive full Downlink slots. Supported: [0-80].
      - **nof_dl_symbols**: Optional INT (0). Number of Downlink symbols at the beginning of the slot following full Downlink slots. Supported: [0-13].
      - **nof_ul_slots**: Optional INT (3). Number of consecutive full Uplink slots. Supported: [0 - 80].
      - **nof_ul_symbols**: Optional INT (0). Number of Uplink symbols at the end of the slot preceding the first full Uplink slot. Supported: [0-13].

  paging
    - Further optional parameters to configure the paging configuration parameters. 

      - **pg_search_space_id**: Optional UINT (1). Sets the SearchSpace to use for Paging. Supported: [0, 1]. 
      - **default_pg_cycle_in_rf**: Optional UINT (128). Sets the default Paging cycle in nof. Radio Frames. Supported: [32,64,128,256]. 
      - **nof_pf_per_paging_cycle**: Optional TEXT (oneT). Sets the number of paging frames per DRX cycle. Supported: [oneT,halfT,quarterT,oneEighthT,oneSixteethT]. 
      - **pf_offset**: Optional UINT (0). Sets the paging frame offset. Supported: [0 - (nof_pf_per_paging_cycle - 1)].
      - **nof_po_per_pf**: Optional UINT (1). Sets the number of paging occasions per paging frame. Supported: [1, 2, 4]. 

  csi
    - Further optional parameters to configure the CSI configuration parameters. 

      - **pwr_ctrl_offset**: Optional INT (0). Sets the power offset of PDSCH RE to NZP CSI-RS RE in dB. Supported: [-8 - +15]. 

.. _manual_config_ref_log: 

log
===

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
    - Optional TEXT (info). Sets radio log level.

  fapi_level
    - Optional TEXT (warning). Sets FAPI log level.

  ofh_level
    - Optional TEXT (warning). Sets Open Fronthaul log level.

  f1ap_level
    - Optional TEXT (warning). Sets F1AP log level.

  f1u_level
    - Optional TEXT (warning). Sets F1u log level.

  du_level
    - Optional TEXT (warning). Sets DU log level.

  cu_level
    - Optional TEXT (warning). Sets CU log level.
    
  sec_level
    - Optional TEXT (warning). Sets security functions level.

  lib_level
    - Optional TEXT (warning). Sets generic log level.

  hex_max_size
    - Optional UINT (0). Sets maximum number of bytes to print for hex messages. Supported: [0 - 1024].

  broadcast_enabled
    - Optional BOOL (false). Enables logging in the PHY and MAC layer of broadcast messages and all PRACH opportunities.

  phy_rx_symbols_filename
    - Optional TEXT. Print received symbols to file. Symbols will be printed if a valid path is set. Format: file path.

.. _manual_config_ref_pcap:

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

  e1ap_enable
    - Optional BOOL (false). Enable/disable E1AP packet capture.

  e1ap_filename
    - Optional TEXT (/tmp/gnb_e1ap.pcap). Path for E1AP PCAPs.

  f1ap_enable
    - Optional BOOL (false). Enable/disable F1AP packet capture.
    
  f1ap_filename
    - Optional TEXT (/tmp/gnb_f1ap.pcap). Path for F1AP PCAPs.


expert_phy
==============

  nof_pdsch_threads
    - Optional UINT (1). Sets the number of threads for encoding PDSCH. Default value of one for no concurrency acceleration in the PDSCH encoding. Format: Positive integer greater than 0.

  nof_ul_threads
    - Optional UINT (4). Sets number of threads for processing PUSCH and PUCCH. It is set to 4 by default unless the available hardware concurrency is limited in which case will use a minimum of one thread.

  pusch_dec_max_iterations
    - Optional UINT (6). Sets the number of PUSCH LDPC decoder iterations. Format: Positive integer greater than 0.

  pusch_dec_enable_early_stop
    - Optional BOOL (true). Enables the PUSCH decoder early stopping mechanism.

  low_phy_dl_throttling
    - Optional FLOAT (0). Enables throttling of the lower PHY DL baseband generation. Supported: [0, 1]
  
test_mode
=========

  test_ue
    - Optional command to generate automatically created UE for testing purposes

      - **rnti**: Optional ENUM (0). Sets the C-RNTI of the UE. Supported: [0 - 65519].
      - **pdsch_active**: Optional BOOLEAN (1). Enables the PDSCH of the UE.
      - **pusch_active**: Optional BOOLEAN (1). Enables the PUSCH of the UE.
<<<<<<< HEAD
=======
      - **cqi**: Optional UINT (15). Sets the Channel Quality Information to be forwarded to the test UE. Supported: [1 - 15]. 
      - **pmi**: Optional UINT (0). Sets the Precoder Matrix Indicator to be forwarded to test UE. Supported: [0 - 3]. 
      - **ri**: Optional UINT (1). Sets the Rank Indicator to be forwarded to the test UE. Supported: [1 - 2]. 

>>>>>>> d8fbbd4 (config_ref: update to match latest code)
