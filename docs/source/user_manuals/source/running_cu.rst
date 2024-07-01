If srsRAN Project has been installed using ``sudo make install`` or installed from packages then you will be able to run srsCU from anywhere on your machine. 

If you built srsRAN Project from source and have not installed it, then you can run srsCU from: ``/srsRAN_Project/build/apps/cu``. In this folder you will find the srsCU application binary. 

Run srsCU as follows, passing the YAML configuration file:  

.. code-block:: bash

   sudo ./srsCU -c cu.yml
   
Run srsCU with ``sudo`` to ensure threads are configured with the correct priority. 

Example configuration files can be found in the ``configs/`` folder in the srsRAN Project codebase. For more information on the configuration files and the available parameters see the :ref:`configuration reference <manual_config_ref>`.

When running, srsCU should generate the following console output:

.. code-block:: bash

    N2: Connection to AMF on 127.0.1.100:38412 completed
    F1-C: Listening for new connections on 127.0.10.1:38471...

    ==== CU started ===
    Type <h> to view help   

Configuration parameters can also be passed on the command line. To see the list of options, use: 

.. code-block:: bash

   ./srscu --help