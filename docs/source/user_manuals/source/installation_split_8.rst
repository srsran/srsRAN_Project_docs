
.. note:: 

    srsRAN Project allows for compile time selection of a Split 7.2 or Split 8 configuration. By default, srsRAN Project builds with both options enabled. If you want to compile with the option to have both Split configurations available, follow the "Vanilla" installation guide. 

First, clone the srsRAN Project repository: 

.. code-block:: bash

    git clone https://github.com/srsRAN/srsRAN_Project.git

Then build the code-base, making sure to pass the correct CMake flag: 

.. code-block:: bash 

    cd srsRAN_Project
    mkdir build
    cd build
    cmake -DDU_SPLIT_TYPE=SPLIT_8  ../ 
    make -j $(nproc)
    make test -j $(nproc) 

You can now run the gNB from ``srsRAN_Project/build/apps/gnb/``. If you wish to install the srsRAN Project gNB, you can use the following command: 

.. code-block:: bash

    sudo make install
