"""Information about the SDMX-ML 2.1 file format."""
from sdmx.model import v21

from .common import XMLFormat

FORMAT = XMLFormat(
    model=v21,
    base_ns="http://www.sdmx.org/resources/sdmxml/schemas/v2_1",
    class_tag=[
        ("message.DataMessage", "mes:GenericData"),
        ("message.DataMessage", "mes:GenericTimeSeriesData"),
        ("message.DataMessage", "mes:StructureSpecificTimeSeriesData"),
        ("model.NoSpecifiedRelationship", "str:None"),
        ("model.DataflowDefinition", "str:Dataflow"),
        ("model.MetadataflowDefinition", "str:Metadataflow"),
    ]
    + [
        (f"model.{name}", f"str:{name}")
        for name in "ContentConstraint MeasureDimension PrimaryMeasure".split()
    ],
)


def __getattr__(name):
    return getattr(FORMAT, name)
