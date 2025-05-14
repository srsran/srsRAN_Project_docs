.. _manual_running:

Running |project_name|
######################

.. note:: 

   This guide outlines running |project_name| applications in a Split 8 deployment with a USRP, for Split 7.2 deployments see :ref:`here <oran_ru_tutorial>`. 

Baseline Requirements
*********************

To successfully run an end-to-end network |project_name| applications you will need the following: 

    - A PC with a Linux based OS (Ubuntu 22.04 or later)
    - A USRP device
    - |project_name| (see the :ref:`Installation Guide <manual_installation_build>`)
    - A 3rd-party 5G core (we recommend `Open5GS <https://github.com/open5gs/open5gs>`_)
    - A 3rd-party 5G UE

Recommended: 

    - External clock source 

If you plan to connect the gNB to a COTS UE we recommend that you use an external clock source such as an Octoclock or GPSDO that is compatible with your RF-frontend, as the on-board clock within the USRP may not be accurate enough to enable a connection with the UE.
This is discussed further in the relevant tutorial. 

----

System Preparation
******************

Before running any of |project_name| applications, we recommend tuning your system for best performance. We provide a script to configure known performance parameters:

   - `srsRAN performance script <https://github.com/srsran/srsRAN_Project/tree/main/scripts/srsran_performance>`_

The script does the following: 

   1. Sets the scaling governor to performance
   2. Disables DRM KMS polling
   3. Tunes network buffers (Ethernet based USRPs only)
   
Run the script as follows from the main project folder:

.. code-block:: bash

   sudo ./scripts/srsran_performance

----

Running |project_name|
**********************

.. tabs:: 

   .. tab:: srsGNB 

      .. include:: running_gnb.rst

   .. tab:: srsCU  

      .. include:: running_cu.rst 

   .. tab:: srsDU  

      .. include:: running_du.rst 

For more information on running |project_name|, and configuring for various use-cases see the :ref:`full list of tutorials <tutorials>`.  