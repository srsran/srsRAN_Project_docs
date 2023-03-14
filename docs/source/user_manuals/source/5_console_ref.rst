.. _manual_console_ref: 

Console Reference
#################

The gNB application runs in the console. When running, type ``t`` in the console to enable the metrics trace.

A sample output showing bi-directional traffic can be seen here:

.. code-block:: bash

              -------------DL----------------|------------------UL--------------------
    pci rnti  cqi  mcs  brate   ok  nok  (%) | pusch  mcs  brate   ok  nok  (%)    bsr
      1 4601   15   28   139M  867    0   0% |  29.4   28   133M  779    0   0%   150k
      1 4601   15   28   138M  851   10   1% |  29.5   28   121M  704    6   0%   150k
      1 4601   15   28   138M  863    0   0% |  29.5   28   133M  778    0   0%   150k
      1 4601   15   28   139M  869    0   0% |  29.3   28   134M  781    0   0%   150k
      1 4601   15   28   130M  800   10   1% |  29.8   28   131M  745    2   0%   150k
      1 4601   15   28   138M  855    8   0% |  29.3   28   134M  772    4   0%   150k
      1 4601   15   28   138M  865    0   0% |  28.7   28   133M  778    0   0%   150k
      1 4601   15   28   137M  848   11   1% |  29.7   28   133M  767    2   0%   150k
      1 4601   15   28   135M  838    4   0% |  29.6   28   132M  749    4   0%   150k
      1 4601   15   28   139M  867    0   0% |  29.3   28   133M  779    0   0%   150k
      1 4601   15   28   139M  867    0   0% |  29.6   28   133M  778    0   0%   150k

Metrics are provided on a per-UE basis. The following metrics are provided: 

:pci: `Physical Cell Identifier <https://www.sharetechnote.com/html/Handbook_LTE_PCI.html>`_
:rnti: `Radio Network Temporary Identifier <https://www.sharetechnote.com/html/5G/5G_RNTI.html>`_ (UE identifier)
:cqi: `Channel Quality Indicator <https://www.sharetechnote.com/html/Handbook_LTE_CQI.html>`_ reported by the UE (1-15)
:mcs: `Modulation and coding scheme <https://www.sharetechnote.com/html/5G/5G_MCS_TBS_CodeRate.html>`_ (0-28)
:brate: Bitrate (bits/sec)
:ok: Number of packets successfully sent
:nok: Number of packets dropped
:(%): % of packets dropped
:pusch: PUSCH SINR (Signal-to-Interference-plus-Noise Ratio)
:bsr: `Buffer Status Report <https://www.sharetechnote.com/html/Handbook_LTE_BSR.html>`_ - data waiting to be transmitted as reported by the UE (bytes)
