.. _manual_config_ref:

Configuration Reference
#######################

The srsRAN Project gNB application uses a YAML (.yml) configuration file.

The gNB comes with a number of example configuration files, these can be found in ``srsRAN_Project/configs/`` in the source code:

    - `B200 USRP @ 20 MHz in band 78 (TDD) <https://github.com/srsran/srsRAN_Project/blob/main/configs/gnb_rf_b200_tdd_n78_20mhz.yml>`_
    - `N310 USRP @ 20 MHz in band 3 (FDD) <https://github.com/srsran/srsRAN_Project/blob/main/configs/gnb_rf_n310_fdd_n3_20mhz.yml>`_

These configuration file examples provide a basic set-up to get users up and running, users can easily modify these to suit their use-case.

More example configuration files for various use cases can be found `here <https://github.com/srsran/srsRAN_Project/tree/main/configs>`_.
These include sample supplementary configuration files for: 

  - MIMO with a USRP
  - Increasing QAM from 64 to 256
  - Specific QOS configurations for voice, video, IMS, live-streaming and buffered video streaming
  - Slicing support

These are intended to be used in conjunction with other configuration files, for example you might run the MIMO example as follows: 

.. code-block:: bash

   sudo ./gnb -c gnb_rf_n310_fdd_n3_20mhz.yml -c mimo.yml

Furthermore you may wish to use QAM256 in addition to the above. This can be done as follows: 

.. code-block:: bash

  sudo ./gnb -c gnb_rf_n310_fdd_n3_20mhz.yml -c mimo.yml -c qam256.yml

----

Configuration Reference
***********************

All configuration parameters are presented here below in the following format:

.. code-block:: yaml 

  parameter: default_value         # Optional/Required TYPE (default value). Parameter description. Format: <format description> OR Supported: <supported values>.

.. tabs:: 

  .. tab:: gNB

    .. literalinclude:: .config/configuration.yml
      :language: yaml 

  .. tab:: srsCU

    .. literalinclude:: .config/cu.yml
      :language: yaml 

  .. tab:: srsDU

    .. literalinclude:: .config/du.yml
      :language: yaml 

----

Antenna Configuration
*********************

srsRAN Project supports SISO, codebook-based MIMO, and TX/RX diversity. These options can be configured in the ``cell_cfg`` section via the ``nof_antennas_dl`` and ``nof_antennas_ul`` parameters. 

When you configure ``nof_antennas_dl`` and ``nof_antennas_ul``, it informs the gNB about the number of antennas available for downlink (DL) and uplink (UL) transmissions, respectively. By default, a 
single physical antenna is used for both DL and UL, meaning the values of ``nof_antennas_dl`` and ``nof_antennas_ul`` are not additive.

An example of a MIMO configuration file can be found in the example configuration files provided with the srsRAN Project source files. 