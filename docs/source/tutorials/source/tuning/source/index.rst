.. _tuning:

srsRAN gNB Performance Tuning
#############################

.. note::

   This tutorial does not cover machine-specific configuration steps (e.g., BIOS settings) or the installation and fine-tuning of real-time Linux kernels.

Introduction
************

This tutorial provides a step-by-step guide to tuning a Linux-based machine for maximizing the performance of the srsRAN CU/DU. While optimal performance 
of the srsRAN gNB may require additional machine-specific fine-tuning, the recommendations outlined here are designed to meet the needs of most users.

TuneD
*****

The approach to performance tuning outlined here utilizes `TuneD <https://tuned-project.org/>`_, a system tuning service for Linux that uses ``udev`` to monitor connected devices and 
dynamically adjust system settings according to user-definable profiles. TuneD provides both static and adaptive tuning capabilities, allowing users to optimize 
the performance of the system for specific workloads or environments. For that, the user-definable profiles, amongst others, can include ``GRUB`` 
command-line arguments, CPU tuning parameters and sysf-exposed kernel parameters (e.g. ``kobject``).

Installation
============

The TuneD tool can be installed with the following commands:

.. code-block:: bash

   sudo apt install tuned
   sudo ln -s /boot/grub/grub.cfg /etc/grub2.cfg

Once installed, edit ``/etc/grub.d/00_tuned`` and add the following line at the end of the file:

.. code-block:: bash

   echo "export tuned_params"

srsRAN tuning profile
=====================

Custom profiles can be created to optimize the system performance according to user-specific requirements. It is advised to base those on 
pre-existing real-time profiles (e.g., ``/usr/lib/tuned/realtime/tuned.conf``). As part of this tutorial you can download a custom srsRAN tuning profile, 
aimed at optimizing the gNB performance:

* :download:`srsRAN tuning profile <.config/tuned.conf>`
* :download:`srsRAN tuning script <.config/startup.sh>`

To use the srsRAN tuning profile we recommend creating a new folder inside ``/usr/lib/tuned/`` and copying both files above to it 
(e.g., ``/usr/lib/tuned/srs/``). We also recommend users open the tuning profile and inspect its contents, as extensive in-line comments have been 
added to explain the selected choices. Once the files are copied, please make sure that the script is executable:

.. code-block:: bash

   sudo chmod +x /usr/lib/tuned/srs/startup.sh

Before activating the srsRAN tuning profile you need to make sure that (in case it is installed) the ``power-profiles-daemon`` is disabled:

.. code-block:: bash

   sudo systemctl stop power-profiles-daemon.service
   sudo systemctl disable power-profiles-daemon.service

The srsRAN tuning profile can be activated with the following command:

.. code-block:: bash

   sudo tuned-adm profile srs

The current active tuning profile can be checked at ``/etc/tuned/active_profile`` or with the following command:

.. code-block:: bash

   tuned-adm active

We recommend configuring the TuneD service to automatically start at system startup. You can do this with the following command:

.. code-block:: bash

   sudo systemctl enable tuned.service

Finally, the machine must be rebooted in order for the modified ``GRUB`` arguments to be applied.

Further Reading
================

 - `Performance Tuning Guide - TuneD <https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html-single/performance_tuning_guide/index#chap-Red_Hat_Enterprise_Linux-Performance_Tuning_Guide-Tuned>`_.
 - `Real-time group scheduing <https://www.kernel.org/doc/html/latest/scheduler/sched-rt-group.html>`_.
