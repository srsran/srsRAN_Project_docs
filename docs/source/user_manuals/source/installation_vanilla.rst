First, clone |project_name| repository: 

.. code-block:: bash

    git clone https://github.com/srsRAN/srsRAN_Project.git

Then build the code-base: 

.. code-block:: bash 

    cd srsRAN_Project
    mkdir build
    cd build
    cmake ../ 
    make -j $(nproc)
    make test -j $(nproc) 

You can now run the gNB from ``srsRAN_Project/build/apps/gnb/``. If you wish to install |project_name|, you can use the following command: 

.. code-block:: bash

    sudo make install
