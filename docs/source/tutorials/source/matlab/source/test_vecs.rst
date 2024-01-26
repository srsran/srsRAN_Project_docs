The PHY components of srsRAN Project are tested by feeding each component with vectors of input data and
comparing the resulting output with their expected values. In srsRAN Project, the test vectors for a
PHY component usually consist of a number of binary files with input and output data, and a single shared header file 
that describes the test set-up and the content of the binary files. The binary files are packed in a single tarball.
For example, the test vectors of the channel estimator are provided by the files ``port_channel_estimator_test_data.h`` and
``port_channel_estimator_test_data.tar.gz`` in ``~/srsRAN_Project/tests/unittests/phy/upper/signal_processors``. 

The files ``srs<ComponentName>Unittest.m`` in the main directory of ``srsRAN-matlab`` provide the classes for
generating such PHY input-output test vectors. This is done by leveraging MATLAB 5G Toolbox. These classes inherit from
the MATLAB ``matlab.unittest.TestCase`` class, meaning all of the tools within MATLAB's unit
testing framework can be used with them. To facilitate the generation of test vectors, a simplified interface
is provided with srsRAN-matlab. 

To generate the test vectors for all PHY components the following code needs to be run from the MATLAB console: 

.. code-block:: matlab

   runSRSRANUnittest('all', 'testvector')

This will generate a ``.h`` and ``.tar.gz`` file for each of the PHY components and place them in the folder ``~/srsRAN_matlab/testvector_outputs``.. 

The test vectors for a single PHY component can also be generated. This is done by replacing ``all`` with the name of the desired
component, as per its declaration in ``~/srsRAN_Project/include/srsran/``. For example, the test vectors for the channel estimator, 
whose interface is declared in ``~/srsRAN_Project/include/srsran/phy/upper/signal_processors/port_channel_estimator.h``, can be
generated with the following command: 

.. code-block:: matlab 

   runSRSRANUnittest('port_channel_estimator', 'testvector')

Once the test vectors have been generated, the pairs of ``.h`` and ``tar.gz`` files in the ``testvector_outputs`` folder
can be transferred to the srsRAN Project folder with the MATLAB command:

.. code-block:: matlab

   srsTest.copySRStestvectors('testvector_outputs', '~/srsRAN_Project/')

This command will automatically copy all test vectors to the proper subdirectory inside ``~/srsRAN_Project/tests/unittests/phy``. 

By default, executing ``runSRSRANUnittest`` will reproduce the same test vectors as the ones provided with
the srsRAN Project repository. To generate a random set of vectors, we simply need to add the ``RandomShuffle``
option. This can be done with the following command: 

.. code-block:: matlab

   runSRSRANUnittest('all', 'testvector', RandomShuffle=true)