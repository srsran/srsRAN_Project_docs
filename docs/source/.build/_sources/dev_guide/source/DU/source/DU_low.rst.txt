
.. _DU_low: 

DU-Low
######


The DU-low is composed of the upper PHY module. The upper PHY encodes and decodes transport blocks which are sent/received using the FAPI interface.

The DU-low implements split 7-2x (discussed further :ref:`here <7_2_split>`), which means that the DU-low we can connect any RU device that is compliant with this split.

During the pre-operational stage, the DU manager sends the cell configuration for each cell, and configures the basic parameters of the upper phy to the DU-low. The 
DU-low then manages the state and configuration for each individual cell.

Upper Phy
*********

Overview
========

Implementation
==============
