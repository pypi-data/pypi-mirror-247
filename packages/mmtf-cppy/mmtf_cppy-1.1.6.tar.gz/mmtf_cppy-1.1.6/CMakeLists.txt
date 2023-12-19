cmake_minimum_required(VERSION 3.15...3.26 FATAL_ERROR)


# Version based on repo tag
execute_process(
    COMMAND git describe --exact-match --tags
    OUTPUT_VARIABLE GIT_VERSION
    ERROR_QUIET
)
string(STRIP "${GIT_VERSION}" GIT_VERSION)
string(REGEX REPLACE "^v" "" GIT_VERSION "${GIT_VERSION}")
if ("${GIT_VERSION}" STREQUAL "")
  set(GIT_VERSION "0.0.0")
endif()
project(mmtf-cpp VERSION ${GIT_VERSION} LANGUAGES CXX)
message("Using git to tag version as: ${GIT_VERSION}")

option(mmtf_build_examples "Build the examples" OFF)
SET(MSGPACK_USE_BOOST OFF CACHE BOOL "msgpack-c uses boost by default, lets keep that off")
# option(MSGPACK_USE_BOOST "msgpack-c uses boost by default, lets keep that off" OFF)

add_library(MMTFcpp INTERFACE)
target_compile_features(MMTFcpp INTERFACE cxx_auto_type)

target_include_directories(MMTFcpp INTERFACE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

include(FetchContent)
FetchContent_Declare(
  msgpack-cxx
  GIT_REPOSITORY https://github.com/msgpack/msgpack-c.git
  GIT_TAG cpp-6.1.0)
FetchContent_MakeAvailable(msgpack-cxx)

if(WIN32)
  target_link_libraries(MMTFcpp INTERFACE ws2_32)
endif()

target_link_libraries(MMTFcpp INTERFACE msgpack-cxx)

if (build_py)
  add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/src/python)
endif()


if (BUILD_TESTS)
    enable_testing()
    add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/tests)
endif()

if (mmtf_build_examples)
    add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/examples)
endif()

install(
    DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/include/
    DESTINATION  "include"
    FILES_MATCHING PATTERN "*.hpp")
