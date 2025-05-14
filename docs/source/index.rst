
|project_name| Documentation
#############################

.. image:: .imgs/srsran_arch_5g.png

.. meta::
    :description lang=en:
        Documentation for |project_name|.

|project_name| is an open-source 5G CU/DU from `SRS <https://www.srs.io>`_.

It is a complete RAN solution compliant with 3GPP and O-RAN Alliance specifications. |project_name|  includes the full L1/2/3 stack with minimal external dependencies. The software is portable across processor architectures and
scalable from low-power embedded systems to cloudRAN, providing a powerful platform for mobile wireless research and development.

Get started with |project_name| :

   - :ref:`Install<manual_installation>` |project_name| on your computer.
   - Get up and running with |project_name| :ref:`here<manual_running>`.
   - More advanced users should read the :ref:`Developers Guide <dev_guide>`.
   - Get up to speed on 5G and OpenRAN with our :ref:`Knowledge Base <knowledge_base>`.

Useful resources:

    * |project_name|  `source code <https://github.com/srsran/srsRAN_project>`_.
    * Explore the |project_name|  `Discussions <https://github.com/srsran/srsran_project/discussions>`_ for news and user support.
    * Discover the `srsRAN Enterprise solution <https://srs.io/srsran-enterprise-5g/>`_ for Private 5G network deployments.

----

.. toctree::
   :maxdepth: 1
   :caption: General

   general/source/2_features_and_roadmap.rst
   general/source/3_contributions.rst
   general/source/4_reporting.rst
   general/source/5_release_notes.rst
   general/source/6_dev_status.rst

.. toctree::
   :maxdepth: 1
   :caption: User Manual

   user_manuals/source/installation.rst
   user_manuals/source/running.rst
   user_manuals/source/console_ref.rst
   user_manuals/source/outputs.rst
   user_manuals/source/config_ref.rst
   user_manuals/source/grafana_gui.rst
   user_manuals/source/troubleshooting.rst

.. toctree::
   :maxdepth: 1
   :caption: Developers Guide

   dev_guide/source/software_arch/source/index.rst
   dev_guide/source/code_guide/source/index.rst
   dev_guide/source/testing_policy/source/index.rst
   dev_guide/source/logging_guide/source/index.rst

.. toctree::
   :maxdepth: 1
   :caption: Knowledge Base

   knowledge_base/source/oran_gnb/source/index.rst
   knowledge_base/source/gnb_components/source/index.rst
   knowledge_base/source/gnb_interfaces/source/index.rst
   knowledge_base/source/cots_ues/source/index.rst

.. toctree::
   :maxdepth: 1
   :caption: Tutorials

   tutorials/source/srsUE/source/index.rst
   tutorials/source/cotsUE/source/index.rst
   tutorials/source/amariUE/source/index.rst
   tutorials/source/dpdk/source/index.rst
   tutorials/source/k8s/source/index.rst
   tutorials/source/handover/source/index.rst
   tutorials/source/ntn/source/index.rst
   tutorials/source/cu_du_split/source/index.rst
   tutorials/source/oranRU/source/index.rst
   tutorials/source/near-rt-ric/source/index.rst
   tutorials/source/matlab/source/index.rst
   tutorials/source/tuning/source/index.rst
   tutorials/source/testmode/source/index.rst
   tutorials/source/hw_kit/source/index.rst
