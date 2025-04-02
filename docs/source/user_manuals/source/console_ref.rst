.. _manual_console_ref: 

Console Reference
#################

Both the gNB and DU applications run in the console. When running, type ``t`` in the console to enable the metrics trace.

A sample output showing bi-directional traffic can be seen here:

.. code-block:: bash

            |--------------------DL---------------------|-------------------------UL------------------------------
   pci rnti | cqi  ri  mcs  brate   ok  nok  (%)  dl_bs | pusch  rsrp  ri  mcs  brate   ok  nok  (%)    bsr    ta  phr
     1 4601 |  15   1   28    17M  908    0   0%    44k |  26.7 -21.2   1   28    17M  545    0   0%  39.8k   0us   18
     1 4601 |  15   1   28    18M  966    0   0%      0 |  26.8 -21.3   1   28    17M  547    0   0%      0   0us   18
     1 4601 |  15   1   28    17M  912    0   0%      0 |  26.8 -21.2   1   28    17M  558    0   0%  77.3k   n/a   18
     1 4601 |  15   1   28    17M  913    0   0%   116k |  26.8 -21.2   1   28    17M  542    0   0%   108k   0us   18
     1 4601 |  15   1   28    18M  949    0   0%  28.5k |  26.8 -21.2   1   28    17M  559    0   0%      0   n/a   18
     1 4601 |  15   1   28    18M  936    0   0%      0 |  26.7 -21.2   1   28    17M  549    0   0%   108k   0us   18
     1 4601 |  15   1   28    17M  918    0   0%      0 |  26.6 -21.2   1   28    17M  552    0   0%   108k   n/a   18
     1 4601 |  15   1   28    17M  913    0   0%   110k |  26.6 -21.2   1   28    17M  552    0   0%  28.6k   n/a   18
     1 4601 |  15   1   28    18M  904    0   0%  17.9k |  26.7 -21.2   1   28    17M  547    0   0%   150k   0us   18
     1 4601 |  15   1   28    18M  909    0   0%      0 |  26.5 -21.2   1   28    17M  548    0   0%   150k   n/a   18
     1 4601 |  15   1   28    17M  903    0   0%      0 |  26.5 -21.2   1   28    17M  552    0   0%  55.5k   n/a   18

Metrics are provided on a per-UE basis. The following metrics are provided: 

:pci: `Physical Cell Identifier <https://www.sharetechnote.com/html/Handbook_LTE_PCI.html>`_
:rnti: `Radio Network Temporary Identifier <https://www.sharetechnote.com/html/5G/5G_RNTI.html>`_ (UE identifier)
:cqi: `Channel Quality Indicator <https://www.sharetechnote.com/html/Handbook_LTE_CQI.html>`_ reported by the UE (1-15)
:ri: `Rank Indicator <https://www.sharetechnote.com/html/Handbook_LTE_RI.html>`_ as reported by the UE
:mcs: `Modulation and coding scheme <https://www.sharetechnote.com/html/5G/5G_MCS_TBS_CodeRate.html>`_ (0-28)
:brate: Bitrate (bits/sec)
:ok: Number of packets successfully sent
:nok: Number of packets dropped
:(%): % of packets dropped
:dl_bs: Downlink Buffer Status, data waiting to be transmitted as reported by the gNB (bytes)
:pusch: PUSCH SINR (Signal-to-Interference-plus-Noise Ratio)
:ri: `Rank Indicator <https://www.sharetechnote.com/html/BasicProcedure_LTE_MIMO.html#Rank_Indicatorl>`_ as reported by the gNB
:rsrp: `Reference Signal Received Power <https://www.sharetechnote.com/html/5G/5G_PowerDefinition.html>`_  
:bsr: `Buffer Status Report <https://www.sharetechnote.com/html/Handbook_LTE_BSR.html>`_, data waiting to be transmitted as reported by the UE (bytes)
:ta: `Timing Advance <https://www.sharetechnote.com/html/5G/5G_TimingAdvance.html>`_ in microseconds 
:phr: `Power Headroom <https://www.sharetechnote.com/html/Handbook_LTE_PHR.html>`_ as reported by the UE
