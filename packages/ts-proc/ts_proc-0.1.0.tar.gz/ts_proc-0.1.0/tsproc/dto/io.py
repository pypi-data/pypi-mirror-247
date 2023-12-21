import datetime
import typing
from pathlib import Path
from typing import NamedTuple

from tsproc import settings
from tsproc.dto.types import DetectionLabel, Product, DetectionConfidence


class Input(NamedTuple):
    # Should be something like "path/to/S1A_IW_GRDH_1SDV_20210102T224803_20210102T224828_035965_04368F_4953_COG.SAFE"
    product_path: typing.Union[str, Path]
    # Int that maps to a Product
    product_type: int

    # These are desired properties and may be overriden at a later stage
    # Int that specifies the desired batch size input to our models.
    # Large batch_size results in faster processing and more memory consumption
    batch_size: typing.Optional[int]
    # Int that specifies the desired input image size to our models.
    # Large image_size results in faster processing and more memory consumption
    image_size: typing.Optional[int]


class BBox(NamedTuple):
    x: float  # Object center position in pixel
    y: float  # Object center position in pixel
    width: float  # Object width in pixel
    height: float  # Object height in pixel


class DetectionInfo(NamedTuple):
    latitude: float
    longitude: float


class VesselType(NamedTuple):
    label: str  # I.e. "Refrigerated Cargo Ship"
    probability: float  # 0-1


# The distribution can for all intended purposes can be seen as gaussian.
# However, the spread may not describe a gaussian distribution
class Distributed(NamedTuple):
    mean: float
    std: float


class VesselBeam(Distributed): pass


class VesselLength(Distributed): pass


class VesselVelocity(Distributed): pass


class VesselHeading(Distributed): pass


class VesselInfo(NamedTuple):
    heading: float  # 0-360 clockwise from NORTH as the heading provided by AIS
    velocity: float  # velocity in m/s TODO knob?

    # Most probable vessel class given several factors.
    # May not be the one with the highest probability in the vessel_classes list
    vessel_class: VesselType
    # list most probable vessel types
    # TODO 0-N values in the list, should we limit it or set a static number?
    vessel_classes: typing.List[VesselType]

    # properties as probability distributions
    velocity_dist: VesselVelocity
    length_dist: VesselLength
    beam_dist: VesselBeam
    heading_dist: VesselHeading


class DetectionClass(NamedTuple):
    label: DetectionLabel
    probability: float


class Detection(NamedTuple):
    confidence: DetectionConfidence
    label: DetectionLabel  # Fast exit label
    bbox: BBox
    labels: typing.List[DetectionClass]
    vessel_info: typing.Optional[VesselInfo]


class Error(NamedTuple):
    code: int
    stacktrace: str
    description: str


class Output(NamedTuple):
    version: str  # String denoting version in a semver format, i.e. 1.2 or 1.2.3
    processesing_start_time: datetime.datetime
    processesing_stop_time: datetime.datetime
    description: str  # TODO describe
    product: Product

    # List of strings denoting the classes utilized in the output
    classes: typing.List[DetectionLabel]
    # List of strings denoting the confidences utilized in the output
    confidences: typing.List[DetectionConfidence]

    # All detected ships, oil spill
    detections: typing.List[Detection]
    count: int  # Length of the detections list


class OutputBuilder:

    def __init__(self, **kwargs):
        self._version = settings.VERSION
        self._product = None
        self._labels = [l.name for l in DetectionLabel]
        self._confidences = [c.name for c in DetectionConfidence]
        self._processing_start_time = None
        self._processing_stop_time = datetime.datetime.utcnow()
        for k, v in kwargs.items():
            setattr(self, k, v)

    def build(self) -> Output:
        output = Output(version=self._version,
                        processesing_start_time=self._processing_start_time,
                        processesing_stop_time=self._processing_stop_time,
                        description='test',
                        product=Product.SENTINEL_1_IW_HH_HV,
                        classes=self._labels,
                        confidences=self._confidences,
                        detections=[],
                        count=0,
                        )
        return output
