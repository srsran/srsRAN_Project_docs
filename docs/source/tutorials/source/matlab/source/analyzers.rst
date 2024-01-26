srsRAN-matlab provides some tools to analyze the signal received by the srsRAN gNB and help debugging the uplink channels. These 
can be found in ``apps/analyzers``. In this tutorial, we will focus on the analyzer for PUSCH transmissions; for the other 
analyzers, which are very similar, please follow the instruction in their help text. 

The following shows some of the other analyzer options: 

.. code-block:: matlab

   % The Resource Grid analyzers only plots the energy map of a slot.
   >> help srsResourceGridAnalyzer

   % For analyzing PUCCH transmissions.
   >> help srsPUCCHAnalyzer

   % For analyzing PRACH transmissions.
   >> help srsPRACHAnalyzer

To use the PUSCH analyzer, the gNB needs to be configured to collect IQ samples. This can be done with by adding the following to 
the gNB configuration file: 

.. code-block:: yaml

   log:
     filename: /tmp/gnb.log                         # save the log to a specified file
     phy_level: debug                               # debug log level for PHY layer set to debug
     phy_rx_symbols_filename: /tmp/iq.bin           # save IQ samples to a specified file

The gNB can then be run as normal. The IQ samples will then be generated. This can be done with the following command: 

.. code-block:: bash

   sudo ./gnb -c config.yml

.. note:: 

   The generated IQ samples will occupy a large amount of disk space. It is recommended to not run the gNB with this configuration for too long.

After running the gNB, open the ``gnb.log`` and locate a PUSCH transmission to analyze. The following example shows the PUSCH transmission that will be 
analyzed in this tutorial: 

.. code-block:: bash 

   2023-10-08T19:14:54.738749 [Upper PHY] [I] [  690.17] RX_SYMBOL: sector=0 offset=79705 size=8568
   2023-10-08T19:14:54.738854 [UL-PHY1 ] [D] [  690.17] PUSCH: rnti=0x4601 h_id=0 prb=[3, 6) symb=[0, 14) mod=QPSK rv=0 tbs=11 crc=OK iter=1.0 sinr=20.1dB t=182.0us
      rnti=0x4601
      h_id=0
      bwp=[0, 51)
      prb=[3, 6)
      symb=[0, 14)
      oack=0
      ocsi1=0
      part2=entries=[]
      alpha=0.0
      betas=[0.0, 0.0, 0.0]
      mod=QPSK
      tcr=0.1171875
      rv=0
      bg=2
      new_data=true
      n_id=1
      dmrs_mask=00100001000100
      n_scr_id=1
      n_scid=false
      n_cdm_g_wd=2
      dmrs_type=1
      lbrm=3168bytes
      slot=690.17
      cp=normal
      nof_layers=1
      ports=0
      dc_position=306
      crc=OK
      iter=1.0
      max_iter=1
      min_iter=1
      nof_cb=1
      sinr_ch_est=26.9dB
      sinr_eq=23.9dB
      sinr_evm[sel]=20.1dB
      evm=0.06
      epre=+22.7dB
      rsrp=+22.7dB
      t_align=-0.2us

Once the transmission has been located and selected, its description can be used to populate configuration options in the srsRAN-matlab analyzer. 

From the MATLAB console, run the following command: 

.. code-block:: matlab 

   cd apps/analyzers
   [carrier, pusch, extra] = srsParseLogs

You will then see the following output: 

.. code-block:: matlab

   Copy the relevant section of the logs to the system clipboard (typically select and Ctrl+C), then switch back to MATLAB and press any key.
   Parsing the following log section:

You should then copy the selected PUSCH transmission details from the log file, and paste it directly into the MATLAB console. The output should look like the following: 

.. code-block:: matlab 

   2023-10-08T19:14:54.738854 [UL-PHY1 ] [D] [  690.17] PUSCH: rnti=0x4601 h_id=0 prb=[3, 6) symb=[0, 14) mod=QPSK rv=0 tbs=11 crc=OK iter=1.0 sinr=20.1dB t=182.0us
     rnti=0x4601
     h_id=0
     bwp=[0, 51)
     prb=[3, 6)
     symb=[0, 14)
     oack=0
     ocsi1=0
     part2=entries=[]
     alpha=0.0
     betas=[0.0, 0.0, 0.0]
     mod=QPSK
     tcr=0.1171875
     rv=0
     bg=2
     new_data=true
     n_id=1
     dmrs_mask=00100001000100
     n_scr_id=1
     n_scid=false
     n_cdm_g_wd=2
     dmrs_type=1
     lbrm=3168bytes
     slot=690.17
     cp=normal
     nof_layers=1
     ports=0
     dc_position=306
     crc=OK
     iter=1.0
     max_iter=1
     min_iter=1
     nof_cb=1
     sinr_ch_est=26.9dB
     sinr_eq=23.9dB
     sinr_evm[sel]=20.1dB
     evm=0.06
     epre=+22.7dB
     rsrp=+22.7dB
     t_align=-0.2us

The function will show the log for confirmation and ask for the sub-carrier spacing and the number of RBs in the resource grid: 

.. code-block:: matlab 

   Do you want to continue? [Y]/N y
   Subcarrier spacing in kHz: 30
   Grid size as a number of RBs: 51

Finally, ``srsParseLogs`` returns an nrCarrierConfig object, `carrier`, an nrPUSCHConfig object, `pusch`, and the `extra` structure with 
additional information about the PUSCH transport block. It should look like the following: 

.. code-block:: matlab 

   carrier = 

     nrCarrierConfig with properties:

                 NCellID: 1
       SubcarrierSpacing: 30
            CyclicPrefix: 'normal'
               NSizeGrid: 51
              NStartGrid: 0
                   NSlot: 17
                  NFrame: 690

      Read-only properties:
          SymbolsPerSlot: 14
        SlotsPerSubframe: 2
           SlotsPerFrame: 20

   pusch = 

     nrPUSCHConfig with properties:

                 NSizeBWP: 51
                NStartBWP: 0
               Modulation: 'QPSK'
                NumLayers: 1
              MappingType: 'A'
         SymbolAllocation: [0 14]
                   PRBSet: [3 4 5]
       TransformPrecoding: 0
       TransmissionScheme: 'nonCodebook'
          NumAntennaPorts: 1
                     TPMI: 0
         FrequencyHopping: 'neither'
        SecondHopStartPRB: 1
            BetaOffsetACK: 20
           BetaOffsetCSI1: 6.2500
           BetaOffsetCSI2: 6.2500
               UCIScaling: 1
                      NID: 1
                     RNTI: 17921
                   NRAPID: []
                     DMRS: [1x1 nrPUSCHDMRSConfig]
               EnablePTRS: 0
                     PTRS: [1x1 nrPUSCHPTRSConfig]

   extra = 

     struct with fields:

                         RV: 0
             TargetCodeRate: 0.1172
       TransportBlockLength: 88
                 dcPosition: 306

The final step is to run the PUSCH analyzer, providing as inputs the objects just created by ``srsParseLogs``,
the path to the IQ record, the offset and the length of the slot (both expressed as a number of IQ samples).
Both the offset and the length of the slot can be found in the log file, on a line like the following one

.. code-block:: matlab

   2023-10-08T19:14:54.738749 [Upper PHY] [I] [  690.17] RX_SYMBOL: sector=0 offset=79705 size=8568

.. note::  
   
   The slot ID (``[  690.17]`` in our example) should be the same as that of the PUSCH log.

The command to run the PUSCH analyzer from the MATLAB console is: 


.. code-block:: matlab 

   srsPUSCHAnalyzer(carrier, pusch, extra, '/tmp/iq.bin', 79705, 8568)
   The block CRC is OK.

This should then output figures displaying the slot energy distribution, the magnitude of the estimated channel, the phase of 
the estimated channel, the equalized constellation and the received soft bit distribution. 

The following figures show these: 

+----------------------------------+------------------------------------+--------------------------------+
|     Slot Energy Distribution     | Magnitude of the Estimated Channel | Phase of the Estimated Channel |
+==================================+====================================+================================+
| .. figure:: .imgs/energy_map.png | .. figure:: .imgs/magnitude.png    | .. figure:: .imgs/phase.png    |
|    :align: center                |    :align: center                  |    :align: center              |
|    :width: 100%                  |    :width: 60%                     |    :width: 60%                 |
+----------------------------------+------------------------------------+--------------------------------+

+-------------------------------------+--------------------------------+
| .. figure:: .imgs/constellation.png | .. figure:: .imgs/soft_bit.png |
|    :align: center                   |    :align: center              |
|    :width: 75%                      |    :width: 90%                 |
+-------------------------------------+--------------------------------+
