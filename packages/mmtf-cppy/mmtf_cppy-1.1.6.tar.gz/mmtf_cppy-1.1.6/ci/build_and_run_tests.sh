set -e
mkdir build && cd build
cmake $CMAKE_ARGS -G Ninja -Dmmtf_build_examples=ON -DBUILD_TESTS=ON -DCMAKE_BUILD_TYPE=debug ..
ninja
./tests/mmtf_tests
./tests/multi_cpp_test
./examples/mmtf_demo ../submodules/mmtf_spec/test-suite/mmtf/173D.mmtf
./examples/traverse ../submodules/mmtf_spec/test-suite/mmtf/173D.mmtf
./examples/traverse ../submodules/mmtf_spec/test-suite/mmtf/173D.mmtf json
./examples/traverse ../submodules/mmtf_spec/test-suite/mmtf/173D.mmtf print
./examples/print_as_pdb ../submodules/mmtf_spec/test-suite/mmtf/173D.mmtf
