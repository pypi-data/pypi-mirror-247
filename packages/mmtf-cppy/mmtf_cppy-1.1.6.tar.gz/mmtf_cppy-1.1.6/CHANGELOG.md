# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).


## [Released]
## v1.1.1 - 2023-12-15
Add Python pybind11 bindings + Upgrade ci/cd
The project can be found on pypi as mmtf_cppy
    
### Added
This PR adds python bindings as well as updates the backend build
process of the mmtf-cpp library significantly.  These improvements are
mainly from a convenience perspective and include:
- Removing all build-based submodules
- Moving to cmake fetchcontent build
- Simplify CMakeLists with better linking procedures
- Upgrade msgpack-c
- Upgrade catch2
- Move to github actions for ci/cd
- Use cibuildwheel for wheel cd

Pybind11 library:
The pybind11 library utilizes the c++ code of mmtf-cpp in order to build
an extremely fast cpp layer underneath the python interface.  You have
to keep in mind that moving between c++ and python is slow, but this is
still much faster than the previously existing python library. see this
example:

time to load a single mmtf file 1000x
cpp bare 0.29s
this library 0.44s
python og 4.34s

## [Unreleased]

## v1.1.0 - 2022-10-03
### Added
- New mapDecoderFrom.. functions to decode only part of an MMTF file
- Support for extra fields in MMTF files according to the
  [latest MMTF specification](https://github.com/rcsb/mmtf/pull/36).
- Support for binary strategy 16 (Run-length encoded 8-bit array),
  bondResonanceList field and optional groupType.bondAtomList &
  groupType.bondOrderList according to the proposed version 1.1 of the
  [MMTF specification](https://github.com/rcsb/mmtf/pull/35).
- New methods to find polymer chains and HETATM following discussions in
  [rcsb/mmtf#28](https://github.com/rcsb/mmtf/issues/28).
- Altered submodule locations [rcsb/mmtf-cpp#37](https://github.com/rcsb/mmtf-cpp/pull/37)
  from the base directory to the new submodules directory.

## v1.0.0 - 2019-02-05
### Added
- Initial release including decoder and encoder for the
  [MMTF specification 1.0](https://github.com/rcsb/mmtf/blob/v1.0/spec.md).

[Unreleased]: https://github.com/rcsb/mmtf-cpp/compare/v1.1.0...HEAD
