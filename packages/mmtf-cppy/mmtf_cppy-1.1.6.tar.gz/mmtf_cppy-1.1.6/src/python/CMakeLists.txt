if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

FetchContent_Declare(
    pybind11
    GIT_REPOSITORY https://github.com/pybind/pybind11.git
    GIT_TAG        v2.11.1)
FetchContent_MakeAvailable(pybind11)
find_package(pybind11 CONFIG REQUIRED)

find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)

Python_add_library(mmtf_bindings MODULE bindings.cpp WITH_SOABI)

target_include_directories(mmtf_bindings PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/../../include
)
target_link_libraries(mmtf_bindings PRIVATE pybind11::headers MMTFcpp)
target_compile_definitions(mmtf_bindings PRIVATE VERSION_INFO=${SKBUILD_PROJECT_VERSION})
install(TARGETS mmtf_bindings DESTINATION mmtf_cppy)
