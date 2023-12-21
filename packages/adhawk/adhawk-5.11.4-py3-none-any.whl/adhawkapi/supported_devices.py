'''This module lists the supported AdHawk devices'''

# List of supported devices (USB vendor id, USB device id)
SUPPORTED_DEVICES = [(0x03eb, 0x2404, ''),
                     (0x03ec, 0x2404, ' (v2)'),
                     (0x03ed, 0x2404, ' (v3)'),
                     (0x32bc, 0x0110, ' (v3)'),  # single-mcu-v1
                     (0x32bc, 0x0111, ' (v3)'),  # single-mcu-3pd
                     (0x32bc, 0x0202, ' (v3)'),  # L5-dev-shield-v1
                     (0x32bc, 0x0204, ' (v3)'),  # dev-board-v4
                     (0x32bc, 0x0301, ' (v3)'),  # AHSM3-ET
                     (0x32bc, 0x0302, ' (v3)'),  # AHSM3-spi-adapter
                     (0x32bc, 0x0112, ' (v3)'),  # L5-evk-v1
                     (0x32bc, 0x0205, ' (v3)'),  # dev-board-v5
                     (0x32bc, 0x0303, ' (v3)'),  # zapata_v1
                     (0x32bc, 0x0113, ' (v3)'),  # EVK4
                     (0x32bc, 0x0304, ' (v3)'),  # ambon_shield
                     (0x32bc, 0x0207, ' (v3)'),  # dev-board-v6
                     (0x32bc, 0x0305, ' (v3)'),  # integration_board_v1
                     (0x32bc, 0x0306, ' (v3)'),  # merlin22 and merlin2
                     (0x32bc, 0x0307, ' (v3)')]  # low_power_integration_board_v1

# List of supported embedded host devices (USB vendor id, USB device id)
EMBEDDED_HUB_DEVICE = (0x0424, 0x03803, '')
