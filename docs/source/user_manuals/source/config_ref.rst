.. _manual_config_ref:

Configuration Reference
#######################

|project_name| uses a YAML (.yml) configuration file.

The gNB comes with a number of example configuration files, these can be found in the ``configs/`` folder in the source files.

These configuration file examples provide a basic set-up to get users up and running, users can easily modify these to suit their use-case.

These include sample supplementary configuration files for: 

  - MIMO with a USRP
  - Increasing QAM from 64 to 256
  - Specific QOS configurations for voice, video, IMS, live-streaming and buffered video streaming
  - Slicing support

|project_name| allows configuration files to be used in concatenated with other configuration files, using the ``-c`` between configuration file. For example you might want to use both the n310 and MIMO example configs together as follows: 

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

|project_name| supports SISO, codebook-based MIMO, and TX/RX diversity. These options can be configured in the ``cell_cfg`` section via the ``nof_antennas_dl`` and ``nof_antennas_ul`` parameters. 

When you configure ``nof_antennas_dl`` and ``nof_antennas_ul``, it informs the gNB about the number of antennas available for downlink (DL) and uplink (UL) transmissions, respectively. By default, a 
single physical antenna is used for both DL and UL, meaning the values of ``nof_antennas_dl`` and ``nof_antennas_ul`` are not additive.

As shown above, an example of a MIMO configuration file can be found in the example configuration files provided with |project_name| source files. 