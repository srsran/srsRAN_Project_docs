
This example demonstrates how to test the throughput and BLER performance of the srsRAN gNB's own PUSCH processor using srsRAN-matlab simulators. By leveraging MATLAB's 5G Toolbox
we can build a simulation set-up that is as close as possible to the one required by 3GPP conformance tests (see TS38.104 and TS38.141). Although not fully representative 
of a real-world deployment with RUs and over-the-air transmission, these simulation are useful for obtaining a first estimation of the performance of the system.

**Compiling the MEXs**

The inclusion of srsRAN Project PHY blocks into a MATLAB simulator is achieved by means of `MEX
functions <https://www.mathworks.com/help/matlab/call-mex-file-functions.html>`_, which are small C++ libraries that can be called from MATLAB. Therefore, the first step for running
the srsRAN-matlab simulators is to build the MEX executables.

First, we compile srsRAN Project with the ``ENABLE_EXPORT`` flag, to export (some of) its libraries for external
projects. This can be done from the command line with the following command: 

.. code-block:: bash 

   cd ~/srsRAN_Project
   cmake -B buildExport -DENABLE_EXPORT:BOOL=ON
   cmake --build buildExport -j 'nproc'

This builds srsRAN Project inside ``buildExport`` and generates the file ``buildExport/srsran.cmake``, which 
provides all the details required to import the necessary srsRAN CMake targets from external projects. 

.. note:: 

   The ``ENABLE_EXPORT`` flag implies the generation of position-independent code (with the ``-fPIC`` compiler option) - as 
   a result, you may experience reduced performance when running the gNB.

The MEX libraries should now be built for srsRAN-matlab. From the command line, run the following: 

.. code-block:: bash

   cd ~/srsRAN_matlab/+srsMEX/source 
   cmake -B buildMEX -DSRSRAN_BINARY_DIR:PATH="~/srsRAN_Project/buildExport" -DMatlab_ROOT_DIR:PATH="/path/to/MATLAB/R2023a"
   cmake --build buildMEX -j 'nproc'

To check that the above was run successfully, execute the following command from the main srsRAN-matlab directory:

.. code-block:: 

   runtests('unitTests', Tag='mex code')

This should output the following, or similar: 

.. code-block:: matlab 

    ans = 

      1x45 TestResult array with properties:

        Name
        Passed
        Failed
        Incomplete
        Duration
        Details

    Totals:
       6 Passed, 0 Failed, 39 Incomplete.
       14.7124 seconds testing time.

You can then run: 

.. code-block:: matlab 

    runSRSRANUnittest('all', 'testmex')

If successful, the ``runSRSRANUnittest`` will generate test vectors, these will be fed into the MEX versions of the srsRAN Project PHY components. An output similar to the following will be shown: 

.. code-block:: matlab 

    Failure Summary:

         Name                                                                                                                                                                                         Failed  Incomplete  Reason(s)
        ==========================================================================================================================================================================================================================================
         srsPRACHDetectorUnittest[RandomDefault=true#ext,outputPath=_home_david_Code_MATLAB_srsgnb_matlab_testvector_outputs#ext]/mexTest(DuplexMode=FDD,PreambleFormat=1,UseZCZ=false,nAntennas=1)               X       Filtered by assumption.
        ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
         srsPRACHDetectorUnittest[RandomDefault=true#ext,outputPath=_home_david_Code_MATLAB_srsgnb_matlab_testvector_outputs#ext]/mexTest(DuplexMode=FDD,PreambleFormat=1,UseZCZ=false,nAntennas=2)               X       Filtered by assumption.
        ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    ...

         srsPRACHDetectorUnittest[RandomDefault=true#ext,outputPath=_home_david_Code_MATLAB_srsgnb_matlab_testvector_outputs#ext]/mexTest(DuplexMode=TDD,PreambleFormat=A1,UseZCZ=true,nAntennas=2)               X       Filtered by assumption.
        ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
         srsPRACHDetectorUnittest[RandomDefault=true#ext,outputPath=_home_david_Code_MATLAB_srsgnb_matlab_testvector_outputs#ext]/mexTest(DuplexMode=TDD,PreambleFormat=A1,UseZCZ=true,nAntennas=4)               X       Filtered by assumption.

Where only ``Incomplete`` tests should show. If a test shows as ``Failed`` an error has occurred. 

**Running the PUSCH Simulator**

In the MATLAB console, from the main srsRAN-matlab directory, a simulator object can be created as follows:

.. code-block:: matlab 

   cd apps/simulators/PUSCHBLER
   sim = PUSCHBLER

This should give the following output: 

.. code-block:: matlab 

   sim = 

     PUSCHBLER with properties:

      Configuration
                            NCellID: 1
                               RNTI: 1
                  SubcarrierSpacing: 15
                       CyclicPrefix: 'Normal'
                          NSizeGrid: 52
                             PRBSet: [0 1 2 3 4 5 6 7 8 9 10 ... ]
                   SymbolAllocation: [0 14]
                        MappingType: 'A'
              DMRSConfigurationType: 1
                         DMRSLength: 1
             DMRSAdditionalPosition: 1
                  DMRSTypeAPosition: 2
                           MCSTable: 'qam64'
                           MCSIndex: 0
                            NRxAnts: 1
                            NTxAnts: 1
                          NumLayers: 1
                       DelayProfile: 'AWGN'
            PerfectChannelEstimator: true
                         EnableHARQ: false
                 ImplementationType: 'matlab'
                    QuickSimulation: true
       DisplaySimulationInformation: false
                 DisplayDiagnostics: false

The simulation set-up can now be modified as desired by the user. In particular, the ``ImplementationType`` should be changed to ``srs``. Doing 
so allows the PHY components of srsRAN Project to be used (via the MEX libraries above) instead of those from the MATLAB 5G Toolbox.

This can be done with the following command: 

.. code-block:: matlab

   sim.ImplementationType = 'srs'

A simulation can then be run to evaluate the throughput and BLER of the PUSCH transmission. This can be done by running ``sim([SNR Range], [# Frames])``. An example simulation may look like the following:  

.. code-block:: matlab

   sim(-8:-3, 10) 

The resulting throughput and BLER estimations can then be plot with the following command: 

.. code-block:: matlab

    sim.plot()

This will give the following output: 

+-------------------------------------+--------------------------------+
| .. figure:: .imgs/tp.png            | .. figure:: .imgs/bler.png     |
|    :align: center                   |    :align: center              |
|    :width: 75%                      |    :width: 90%                 |
+-------------------------------------+--------------------------------+


