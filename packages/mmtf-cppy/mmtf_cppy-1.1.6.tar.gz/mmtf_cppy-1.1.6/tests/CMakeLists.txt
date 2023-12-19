
cmake_minimum_required(VERSION 3.5 FATAL_ERROR)

if(EMSCRIPTEN)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -s TOTAL_MEMORY=150994944 -s DISABLE_EXCEPTION_CATCHING=0")
endif()

FetchContent_Declare(
  Catch2
  GIT_REPOSITORY https://github.com/catchorg/Catch2.git
  GIT_TAG        v3.4.0)
FetchContent_MakeAvailable(Catch2)

add_executable(mmtf_tests mmtf_tests.cpp)
target_compile_features(mmtf_tests PRIVATE cxx_auto_type)
if(EMSCRIPTEN)
  target_link_libraries(mmtf_tests Catch2::Catch2 MMTFcpp)
else()
  target_link_libraries(mmtf_tests Catch2::Catch2WithMain MMTFcpp)
endif()

# test for multi-linking
add_executable(multi_cpp_test multi_cpp_test.cpp multi_cpp_test_helper.cpp)
target_compile_features(multi_cpp_test PRIVATE cxx_auto_type)
target_link_libraries(multi_cpp_test MMTFcpp)

set(TEST_RUNNER "none" CACHE STRING "External runner for the tests")

if (${TEST_RUNNER} STREQUAL "node")
    add_test( NAME mmtf_tests COMMAND node mmtf_tests)
else()
    add_test( NAME mmtf_tests WORKING_DIRECTORY ${CMAKE_BINARY_DIR} COMMAND mmtf_tests)
endif()
