from enum import Enum


class DetectionLabel(Enum):
    SHIP = 1
    OIL = 2


class Product(Enum):
    SENTINEL_1_IW_HH_HV = 1
    SENTINEL_1_IW_VV_VH = 2
    SENTINEL_1_EW_HH_HV = 3

    ICEYE_STRIPMAP = 4
    ICEYE_SCAN = 5

    RCM_SCAN_50M_LOW_NOISE = 6

    SENTINEL_2_L1C = 7
    LANDSAT_8_LIGS = 8
    LANDSAT_9_LIGS = 9


class DetectionConfidence(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
