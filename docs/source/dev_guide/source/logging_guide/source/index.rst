.. _dev_guide_logging: 

Logging Style Guide
###################

To ensure consistency in the formatting of the log entries, some rules should be followed by the developers. 
This allows both users and developers to be able to easily read and parse the logs, accelerating problem discovery.

This document describes the logging rules and reasoning behind them in the srsRAN_Project.

Rule 1: Lists of fields only need to be separated by a whitespace “   “
************************************************************************

.. code-block:: bash

   rnti=0x4602 h_id=0 prb=[3, 21) symb=[0, 14) mod=QPSK rv=0 tbs=437 crc=OK iter=2.0 snr=12.8dB t=145.5us

Rule 2: Maintain consistent order between classes of fields 
***********************************************************

There are different classes of fields:
 
   - fields that represent a context (e.g. UE ID, bearer ID, carrier ID) 
   - fields that represent a value (e.g. snr, tbs, etc.)
   - fields that represent a one-time event (e.g. “Received InitialContextSetupRequest”)

Each logging message should have the following structure:

.. code-block:: cpp

   <timestamp> [layer] [log_level] <contextual fields>: <one-time event>. <value fields>

This should result in a message that looks like: 

.. code-block:: bash

   2023-05-22T15:36:33.070813 [RLC     ] [I] DL ue=5 SRB1: TX PDU. dc=data p=1 si=full sn=0 so=0 pdu_len=11 grant_len=11

Rule 3: Order of contextual fields
**********************************

Contextual fields should always follow the order of lower granularity to highest granularity:

For example: 

.. code-block:: bash

   <direction> <ue ids> <bearer ids> proc=\”<procedure>\”.

This should result in a message that looks like: 

.. code-block:: bash

   DL ue=5 SRB1:…

   ue=5 proc=”UE Context Release”:…

Rule 4: For one time events, provide a cause whenever it's unclear what it might be
***********************************************************************************

For example: 

.. code-block:: bash

   2023-05-22T15:36:33.070813 [MAC     ] [I] ue=5: Unable to forward UL-CCCH message to upper layers. Cause: task queue is full.

Rule 5: ASN.1 Messages should be represented using the respective ASN.1 type name.
***********************************************************************************

For instance the RRC ASN.1 message RRC Release should be formatted using the name “RRCRelease”, which corresponds to the ASN.1 type that is going to be stored in 
the DL-CCCH message. This name is distinct from the camelCase name “rrcRelease” and white space separated name “RRC Release” that appears in Wireshark.

Rule 6: Procedures should be identified by the name specified in the TS clauses.
*********************************************************************************

For instance, the procedure “UE Context Setup” (notice the spaces) has associated ASN.1 messages “UEContextSetupRequest”, “UEContextSetupResponse”. According to Rule 1, 
the *ASN.1 messages* should be formatted **without** white spaces, but according to Rule 2, the *procedure* name should be formatted **with** spaces.

Rule 7: Messages with a context that is not formatted are strictly forbidden!
*****************************************************************************

Messages with a context that have **not** been formatted correctly are strictly forbidden.  

General Tips
*********************************************************************

Use prefix loggers or prefix structs with a specified formatter to maintain order/format consistency of contextual fields.

