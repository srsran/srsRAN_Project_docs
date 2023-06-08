.. _manual_troubleshooting: 

Troubleshooting
###############

For support and help using srsRAN Project, check out the community driven `discussion forum <https://github.com/srsran/srsRAN_Project/discussions>`_.

Performance Tuning
******************

The following sections outline key steps to improve gNB performance. 

CPU Performance Mode
====================

The CPU governor of the PC should be set to performance mode to allow for maximum compute power and throughput. This can be configured for e.g. Ubuntu using:

.. code-block:: bash

   echo "performance" | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

It is also recommended that users running on a laptop keep the PC connected to a power-source at all times while running the gNB, as this will avoid performance loss due to CPU frequency scaling on the machine.

Performance Configuration Script
================================

Before running the gNB application, we recommend tuning your system for best performance. We provide a script to configure known performance parameters:

   - `srsran_performance <https://github.com/srsran/srsRAN_Project/tree/main/scripts/srsran_performance>`_
   

The script does the following: 

   1. Sets the scaling governor to performance
   2. Disables DRM KMS polling
   3. Tunes network buffers (Ethernet based USRPs only)
   
Run the script as follows from the main project folder:

.. code-block:: bash

   sudo ./scripts/srsran_performance


USRP Configuration
******************

Users should always ensure that the USRP they are using is running over USB 3.0 or ethernet and correctly configured. If UHD is built from source, users will have multiple example applications available in ``/usr/lib/uhd/examples/``. User can verify 
their USRP is correctly configured by running the ``uhd_benchmark`` application as follows:

.. code-block:: bash

   sudo ./benchmark_rate --rx_rate [rate in Hz] --tx_rate [rate in Hz]

More details can be found in `this <https://kb.ettus.com/Verifying_the_Operation_of_the_USRP_Using_UHD_and_GNU_Radio>`_ guide on the `Ettus Knowledge Base <https://kb.ettus.com/Knowledge_Base>`_. 

USRP Time Calibration
=====================

Incorrect time calibration of a USRP can lead to preventing the gNB from receiving PRACH transmissions. The TX/RX time calibration adjusts the offset between TX and RX processing chains delay in the USRP. This value varies as a function of sampling 
rate, USRP model and UHD version. Users experiencing issues with incorrect time calibration will see a message similar to the following in the logs: 

.. code-block:: bash

   2023-03-08T08:38:34.130365 [UL-PHY0 ] [I] [ 1001.18] PRACH:  rssi=+0.5dB detected_preambles=[{idx=55 ta=-7.29us power=+85.8dB snr=0.0dB}] t=351.3us
   2023-03-08T08:38:34.130377 [FAPI    ] [E] [     0.0] Detected 1 errors in RACH.indication message at slot=1001.18:
      - Property=Timing advance offset in nanoseconds, value=-7291, expected value=[0-2005000]

In the above log the PRACH arrived 7.29 us early to the gNB, which at a sampling rate of 23.04 MHz is approximately 168 samples. The TX/RX offset needs to be adjusted to a higher value than this so that the PRACH arrives within the detection window. This 
can be done by adding the following to the config file under the ``ru_sdr`` options: 

.. code-block:: yaml 
   
   ru_sdr:
      time_alignment_calibration: -170    # This will set an offset of -170 samples

In general, a larger negative value is better as it will make sure the PRACH falls within the detection window. The consequence of increasing this too much is that the effective cell size is reduced (this is not important for a lab set up).

By default the ``time_alignment_calibration`` parameter is set to 0. This means that in most SDR frontends the PRACH will arrive a few samples late within the window. With preamble format 0, there is enough space in the detection window and this does not cause 
any problem. However, if you are trying to set up a very large cell, or using different preamble formats, you might want to set a positive ``time_alignment_calibration`` value such that there is space in the window for UEs far in the cell.  




