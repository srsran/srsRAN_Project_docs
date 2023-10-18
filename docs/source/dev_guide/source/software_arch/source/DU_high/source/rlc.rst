.. _rlc_overview: 

Radio Link Control (RLC)
########################

RLC layer connects the MAC and the F1AP/PDCP, as shown in :numref:`rlcstack`, and provides that transfer services to these layers.

.. _rlcstack:
.. figure:: .imgs/rlc_stack.png
   :scale: 50 %
   :align: center

   RLC stack

It does this, by providing three different modes:

 * **Transparent Mode (TM)**

  TM is used only in control signaling (SRB0 only) and provides data transfer services without modifying the SDUs/PDUs at all.

 * **Unacknowledged Mode (UM)**

  UM can only be used in data traffic (DRBs only) and provides data transfer services with segmentation/reassembly. It is usually used in delay-sensitive and loss-tolerant traffic, as it does not provide re-transmissions.

 * **Acknowledged Mode (AM)**

  :ref:`AM <rlc_am>` can be used in data and control traffic (mandatory for SRBs, optional for DRBs) and provides data transfer services with segmentation and ARQ procedures. This mode is usually used for traffic that is more loss-sensitive, but more delay-tolerant.

-----

.. toctree::
   :maxdepth: 1

   rlc_am.rst   
 
.. Add to TOCTREE when ready 
   rlc_tm.rst
   rlc_um.rst








