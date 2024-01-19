.. _grafana:  

Grafana Metrics GUI
###################

srsRAN allows the reporting and visualization of the CU/DU metrics to a `Grafana <https://grafana.com/oss/grafana/>`_ WebUI. This is done through the use 
of a `Docker <https://www.docker.com/>`_ container that comes as standard with the srsRAN code base, located in the ``~/srsRAN/docker/`` folder. This container allows users 
to bring up the Grafana dashboard in a single command. 

**Further Reading:**

- `Grafana Docs <https://grafana.com/docs/grafana/latest/?pg=oss-graf&plcmt=hero-btn-2>`_

-----

Configuration
*************

To use the Grafana webUI, you will first need to have Docker installed on your system, you will also need to modify the srsRAN CU/DU configuration file to allow the 
reporting of the metrics to the necessary JSON format for use in the webUI. 

Docker
======

Using the Docker Containers included with srsRAN requires ``docker compose`` to be installed on your system. You can read about ``docker compose`` `here <https://docs.docker.com/compose/>`_.  There 
are multiple ways to install this, but the most basic way to do so is to install Docker Desktop. For installing Docker Desktop on linux, take a look at 
the `Docker documentation <https://docs.docker.com/desktop/install/linux-install/>`_. 

.. note::

    We recommend using a Docker Compose V2 or later. 

srsRAN
======

To enable the correct reporting of metrics to the Grafana UI, the srsRAN configuration files needs to be updated to allow the metrics to be output in the correct JSON format and then sent through a udp-socket to the metrics-server,
where it can be parsed and displayed correctly by the GUI.

.. code-block:: yaml

    metrics:
        enable_json_metrics: true       # Enable reporting metrics in JSON format
        addr: 172.19.1.4                # Metrics-server IP
        port: 55555                     # Metrics-server Port

The ``addr`` and ``port`` values defined above mirror those set in the ``docker-compose.yml`` file found in ``~/srsRAN_Project/docker``. Any changes in these values must be kept consistent across both files. 

-----

Launching GUI
*************

To launch the docker image for the Grafana UI, run the following command from the main folder containing srsRAN:  

.. code-block:: bash

    sudo docker compose -f docker/docker-compose.yml up grafana

The following output should be observed:

.. code-block:: bash

    Creating network "docker_ran" with the default driver
    Starting metrics_server ... 
    Starting metrics_server ... done
    Creating grafana        ... done
    Attaching to grafana

Navigating to http://localhost:3300/ in your preferred web browser will allow you to view the UI. 

You can then run srsRAN as normal. As the UE(s) connect to the network you will begin to see an output for each. These figures and graphics will update automatically during runtime, showing plots for each 
UE on the network. 

-----

GUI Output
**********

A sample of the UI output can be seen here: 


.. image:: .imgs/grafana_cots.png

The above figure shows a single COTS UE connected to the network, with different traffic bursts of varying bandwidth being generated using iPerf. The cell bandwidth is 20 MHz.