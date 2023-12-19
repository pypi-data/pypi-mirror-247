try:
    from ._version import version as __version__
    from ._version import version_tuple as version_tuple
except ImportError:
    __version__ = "unknown version"
    version_tuple = (0, 0, "unknown version")

from .structure_data import (
    Entity as Entity,
    GroupType as GroupType,
    Transform as Transform,
    BioAssembly as BioAssembly,
    StructureData as StructureData,
)


from .mmtf_bindings import (
    CPPStructureData as CPPStructureData,
    decode_int8 as decode_int8,
    encodeRunLengthInt8 as encodeRunLengthInt8,
    decodeFromBuffer as decodeFromBuffer,
    encodeDeltaRecursiveFloat as encodeDeltaRecursiveFloat,
    encodeToFile as encodeToFile,
    decodeFromFile as decodeFromFile,
    encodeFourByteInt as encodeFourByteInt,
    encodeToStream as encodeToStream,
    decode_char as decode_char,
    encodeInt8ToByte as encodeInt8ToByte,
    set_bioAssemblyList as set_bioAssemblyList,
    decode_float as decode_float,
    encodeRunLengthChar as encodeRunLengthChar,
    set_entityList as set_entityList,
    decode_int16 as decode_int16,
    encodeRunLengthDeltaInt as encodeRunLengthDeltaInt,
    set_groupList as set_groupList,
    decode_int32 as decode_int32,
    encodeRunLengthFloat as encodeRunLengthFloat,
)
