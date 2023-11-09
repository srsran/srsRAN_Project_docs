### This is not meant for execution but rather as a register reference to be used for altering the original radio init

LOG_INFO "Set expected DU MAC Address for C-Plane Traffic (C0319/C031A)"
/usr/bin/registercontrol -w C031A -x 0x8061
/usr/bin/registercontrol -w C0319 -x 0x5f0ddfaa

LOG_INFO "Set expected DU MAC Address for U-Plane Traffic (C0315/C0316)"
/usr/bin/registercontrol -w C0316 -x 0x8061
/usr/bin/registercontrol -w C0315 -x 0x5f0ddfaa

LOG_INFO "Set required DU VLAN Tag Control Information for uplink U-Plane Traffic (C0318)"
/usr/bin/registercontrol -w C0318 -x 0x5

LOG_INFO "Set expected DU VLAN Tag Control Information for downlink U-Plane Traffic (C0330)"
/usr/bin/registercontrol -w C0330 -x 0x5

LOG_INFO "Set expected DU VLAN Tag Control Information for downlink C-Plane Traffic (C0331)"
/usr/bin/registercontrol -w C0331 -x 0x5

LOG_INFO "Aligning TDD switching relative to downlink and uplink data and with respect to PPS (C0366)"
/usr/bin/registercontrol -w C0366 -x 0x1225

LOG_INFO "Aligning FPGA uplink timing to arrival of uplink frame(C0303)"
/usr/bin/registercontrol -w c0303 -x 0x24

LOG_INFO "Set the Number of Tx's to 4 (C0300)"
/usr/bin/registercontrol -w C0300 -x 0x01010101

LOG_INFO "Enable  udCompHdr option for DL (C0352)"       
/usr/bin/registercontrol -w c0350 -x 0x0   

LOG_INFO "Enable  udCompHdr option for UL (C0352)"       
/usr/bin/registercontrol -w c0351 -x 0x0

LOG_INFO "Enable  udCompHdr option for PRACH (C0352)"
/usr/bin/registercontrol -w c0352 -x 0x0

LOG_INFO "Set PRACH compression disable for FlexRAN (C0353)"
/usr/bin/registercontrol -w C0353 -x 0x1

LOG_INFO "Set Downlink scaling 6 dB for FlexRAN (C0358)"
/usr/bin/registercontrol -w C0358 -x 0x6

LOG_INFO "Set expected RU PRACH Configuration Index (C0322)"
/usr/bin/registercontrol -w C0322 -x 0xE