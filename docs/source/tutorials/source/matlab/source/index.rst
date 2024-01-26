.. _dpdk: 

MATLAB Testing Tools
####################

Overview
************

This tutorial explains the main features of `srsRAN-matlab <https://github.com/srsran/srsRAN_matlab>`_, a MATLAB-based project for testing
srsRAN Project. More specifically, this tutorial will show how to generate a new set of test vectors for the srsRAN
Project tests, how to analyze the uplink IQ samples recorded by srsRAN gNB, and how to run end-to-end,
link-level simulations for testing PHY components of srsRAN Project. This will be done across three independent sections. 

srsRAN-matlab offers three main tools: the test vector generators, the uplink analyzers and the link-level simulators.

Test Vector Generation
======================

Test vectors are mainly used to test, develop and debug the PHY components of the srsRAN Project. This tutorial will show 
how to generate the set of vectors used for unit testing inside the srsRAN repository. As well as outlining how to generate a 
new set of random vectors for broadening the extent of the tests.

Signal Analyzers
================

The signal analyzers are useful for testing the uplink chain of the gNB. Specifically, they provide visual hints about the 
signal quality in the uplink slots.

Simulators
==========

The simulators can be used to estimate the performance of the PHY uplink channels under different configurations and channel 
conditions provided by MATLAB's 3GPP-compliant models.

Set-Up Considerations
*********************

For this application note, the following hardware and software are used:

- A PC with Ubuntu 22.04.3 LTS
- `srsRAN-matlab <https://github.com/srsran/srsRAN_matlab>`_
- `srsRAN Project <https://github.com/srsran/srsRAN_project>`_
- MathWorks `MATLAB <https://www.mathworks.com/products/matlab.html>`_ (R2022b or R2023a) with the `5G Toolbox <https://www.mathworks.com/products/5g.html?s_tid=srchtitle_site_search_1_5g%20toolbox>`_

.. note:: 

   Running the srsRAN-matlab testing suite requires a working copy of MATLAB and its 5G Toolbox

Installation
************

Assuming that srsRAN Project and MATLAB have both been downloaded and installed, the next step is to download srsRAN-matlab.

This can be done with the following command: 

.. code-block:: bash 

   git clone https://github.com/srsran/srsRAN_matlab.git 

.. note:: 

   This tutorial assumes that srsRAN Project is installed in the users come directory. 

Once it has been downloaded, the working directory for srsRAN-matlab should be added to MATLAB's search path. This can be done from the MATLAB console with the following command:

.. code-block:: matlab

   cd ~/srsRAN_matlab
   addpath . 

To verify you have added srsRAN-matlab successfully to MATLAB's search path, run the following command (again from the MATLAB console): 

.. code-block:: matlab

   runtests('unitTests', Tag='matlab code')

If successful, the following output should be shown at the end of the console output: 

.. code-block:: matlab 

   ans = 

     1x94 TestResult array with properties:

       Name
       Passed
       Failed
       Incomplete
       Duration
       Details

   Totals:
      94 Passed, 0 Failed, 0 Incomplete.
      42.2176 seconds testing time.

-----

.. tabs:: 

   .. tab:: Test Vectors 

      .. include:: test_vecs.rst

   .. tab:: Analyzers  

      .. include:: analyzers.rst 

   .. tab:: Simulators

      .. include:: simulators.rst 
