from pathlib import Path
import tempfile
import unittest

import mmtf_cppy
from mmtf_cppy import StructureData
import numpy as np

MMTF_SPEC_DIR = Path(__file__).parent / "../../../submodules/mmtf_spec"
EXTRA_TEST_DATA_DIR = Path(__file__).parent / "../../../temporary_test_data"


class TestMMTF(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_eq_operator(self):
        s1 = StructureData.init_from_file_name(MMTF_SPEC_DIR / "test-suite/mmtf/173D.mmtf")
        s2 = StructureData.init_from_file_name(MMTF_SPEC_DIR / "test-suite/mmtf/173D.mmtf")
        s3 = StructureData.init_from_file_name(MMTF_SPEC_DIR / "test-suite/mmtf/1AUY.mmtf")
        assert s1 == s2
        assert s1 != s3

    def test_roundtrip(self):
        files = [
            MMTF_SPEC_DIR / "test-suite/mmtf/173D.mmtf",
            MMTF_SPEC_DIR / "test-suite/mmtf/1AA6.mmtf",
            MMTF_SPEC_DIR / "test-suite/mmtf/1AUY.mmtf",
            MMTF_SPEC_DIR / "test-suite/mmtf/1BNA.mmtf",
            MMTF_SPEC_DIR / "test-suite/mmtf/1CAG.mmtf",
            MMTF_SPEC_DIR / "test-suite/mmtf/1HTQ.mmtf",
            MMTF_SPEC_DIR / "test-suite/mmtf/1IGT.mmtf",
            MMTF_SPEC_DIR / "test-suite/mmtf/1L2Q.mmtf",
            MMTF_SPEC_DIR / "test-suite/mmtf/1LPV.mmtf",
            MMTF_SPEC_DIR / "test-suite/mmtf/1MSH.mmtf",
            MMTF_SPEC_DIR / "test-suite/mmtf/1O2F.mmtf",
            MMTF_SPEC_DIR / "test-suite/mmtf/1R9V.mmtf",
            MMTF_SPEC_DIR / "test-suite/mmtf/1SKM.mmtf",
            MMTF_SPEC_DIR / "test-suite/mmtf/3NJW.mmtf",
            MMTF_SPEC_DIR / "test-suite/mmtf/3ZYB.mmtf",
            MMTF_SPEC_DIR / "test-suite/mmtf/4CK4.mmtf",
            MMTF_SPEC_DIR / "test-suite/mmtf/4CUP.mmtf",
            MMTF_SPEC_DIR / "test-suite/mmtf/4OPJ.mmtf",
            MMTF_SPEC_DIR / "test-suite/mmtf/4P3R.mmtf",
            MMTF_SPEC_DIR / "test-suite/mmtf/4V5A.mmtf",
            MMTF_SPEC_DIR / "test-suite/mmtf/4Y60.mmtf",
            MMTF_SPEC_DIR / "test-suite/mmtf/5EMG.mmtf",
            MMTF_SPEC_DIR / "test-suite/mmtf/5ESW.mmtf",
            MMTF_SPEC_DIR / "test-suite/mmtf/empty-all0.mmtf",
            MMTF_SPEC_DIR / "test-suite/mmtf/empty-numChains1.mmtf",
            MMTF_SPEC_DIR / "test-suite/mmtf/empty-numModels1.mmtf",
            EXTRA_TEST_DATA_DIR / "all_canoncial.mmtf",
            EXTRA_TEST_DATA_DIR / "1PEF_with_resonance.mmtf",
        ]
        test_tmp_mmtf_filename = Path(self.temp_dir.name) / "test_mmtf.mmtf"
        for filename in files:
            s1 = StructureData.init_from_file_name(filename)
            s1.write_to_file(test_tmp_mmtf_filename)
            s2 = StructureData.init_from_file_name(test_tmp_mmtf_filename)
            s1.check_equals(s2)
            assert s1 == s2

    def test_bad_mmtf(self):
        doesnt_work = [MMTF_SPEC_DIR / "test-suite/mmtf/empty-mmtfVersion99999999.mmtf"]
        for filename in doesnt_work:
            with self.assertRaises(RuntimeError):
                _ = StructureData.init_from_file_name(filename)

    def test_various_throws(self):
        working_mmtf_fn = MMTF_SPEC_DIR / "test-suite/mmtf/173D.mmtf"
        temporary_file = Path(self.temp_dir.name) / "wrk.mmtf"

        sd = StructureData.init_from_file_name(working_mmtf_fn)
        sd.xCoordList = np.append(sd.xCoordList, 0.334)
        with self.assertRaises(RuntimeError):
            sd.write_to_file(temporary_file)

        sd = StructureData.init_from_file_name(working_mmtf_fn)
        sd.yCoordList = np.append(sd.yCoordList, 0.334)
        with self.assertRaises(RuntimeError):
            sd.write_to_file(temporary_file)

        sd = StructureData.init_from_file_name(working_mmtf_fn)
        sd.zCoordList = np.append(sd.zCoordList, 0.334)
        with self.assertRaises(RuntimeError):
            sd.write_to_file(temporary_file)

        sd = StructureData.init_from_file_name(working_mmtf_fn)
        sd.bFactorList = np.append(sd.bFactorList, 0.334)
        with self.assertRaises(RuntimeError):
            sd.write_to_file(temporary_file)

        sd = StructureData.init_from_file_name(working_mmtf_fn)
        sd.numAtoms = 20
        with self.assertRaises(RuntimeError):
            sd.write_to_file(temporary_file)

        sd = StructureData.init_from_file_name(working_mmtf_fn)
        sd.chainIdList = np.append(sd.chainIdList, "xsz")
        with self.assertRaises(RuntimeError):
            sd.write_to_file(temporary_file)

        sd = StructureData.init_from_file_name(working_mmtf_fn)
        sd.chainIdList = sd.chainIdList.astype("<U16")  # TODO should be default
        sd.chainIdList[0] = "IheartMMTF"
        with self.assertRaises(RuntimeError):
            sd.write_to_file(temporary_file)

        sd = StructureData.init_from_file_name(working_mmtf_fn)
        sd.groupList[0].formalChargeList = sd.groupList[0].formalChargeList[:-1]
        with self.assertRaises(RuntimeError):
            sd.write_to_file(temporary_file)

        sd = StructureData.init_from_file_name(working_mmtf_fn)
        sd.groupList[0].atomNameList = sd.groupList[0].atomNameList[:-1]
        with self.assertRaises(RuntimeError):
            sd.write_to_file(temporary_file)

        sd = StructureData.init_from_file_name(working_mmtf_fn)
        sd.groupList[0].elementList = sd.groupList[0].elementList[:-1]
        with self.assertRaises(RuntimeError):
            sd.write_to_file(temporary_file)

        sd = StructureData.init_from_file_name(working_mmtf_fn)
        sd.groupTypeList[0] = 100
        with self.assertRaises(RuntimeError):
            sd.write_to_file(temporary_file)

    def test_DeltaRecursiveFloat(self):
        encoded_data = b"\x00\x00\x00\x0a\x00\x00\x00\x03\x00\x00\x03\xe8\x7f\xffD\xab\x01\x8f\xff\xca"
        decoded_data = np.array([50.346, 50.745, 50.691])
        ret = mmtf_cppy.encodeDeltaRecursiveFloat(decoded_data, 1000)
        assert ret == encoded_data

    def test_RunLengthFloat(self):
        encoded_data = b"\x00\x00\x00\x09\x00\x00\x00\x03\x00\x00\x00\x64\x00\x00\x00\x64\x00\x00\x00\x03"
        decoded_data = np.array([1.0, 1.0, 1.0])
        ret = mmtf_cppy.encodeRunLengthFloat(decoded_data, 100)
        assert ret == encoded_data

    def test_RunLengthDeltaInt(self):
        encoded_data = b"\x00\x00\x00\x08\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x07"
        decoded_data = np.array(range(1, 8))
        ret = mmtf_cppy.encodeRunLengthDeltaInt(decoded_data)
        assert ret == encoded_data

    def test_RunLengthChar(self):
        encoded_data = b"\x00\x00\x00\x06\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x41\x00\x00\x00\x04"
        decoded_data = np.array(list(map(ord, ("A", "A", "A", "A"))), dtype=np.int8)
        ret = mmtf_cppy.encodeRunLengthChar(decoded_data)
        assert ret == encoded_data

    def test_RunLengthInt8(self):
        encoded_data = b"\x00\x00\x00\x10\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x04"
        decoded_data = np.array((2, 2, 2, 2), dtype=np.int8)
        ret = mmtf_cppy.encodeRunLengthInt8(decoded_data)
        assert ret == encoded_data

    def test_Int8(self):
        encoded_data = b"\x00\x00\x00\x02\x00\x00\x00\x05\x00\x00\x00\x00\x07\x06\x06\x07\x07"
        decoded_data = np.array((7, 6, 6, 7, 7), dtype=np.int8)
        ret = mmtf_cppy.encodeInt8ToByte(decoded_data)
        assert ret == encoded_data

    def test_FourByteInt(self):
        encoded_data = b"\x00\x00\x00\x04\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x01\x00\x02\x00\x01\x00\x00\x00\x00\x00\x00\x00\x02"
        decoded_data = np.array((1, 131073, 0, 2), dtype=np.int32)
        ret = mmtf_cppy.encodeFourByteInt(decoded_data)
        assert ret == encoded_data

    # TODO figure out numpy array -> c++ vector string
    # def test_encodeStringVector():
    #     encoded_data = b'\x00\x00\x00\x05\x00\x00\x00\x06\x00\x00\x00\x04B\x00\x00\x00A\x00\x00\x00C\x00\x00\x00A\x00\x00\x00A\x00\x00\x00A\x00\x00\x00'
    #     decoded_data = np.array(("B", "A", "C", "A", "A", "A"))
    #     ret = mmtf_cppy.encodeStringVector(decoded_data, 4)
    #     assert ret == encoded_data

    def test_atomProperties(self):
        working_mmtf_fn = MMTF_SPEC_DIR / "test-suite/mmtf/173D.mmtf"
        tmp_output_fn = Path(self.temp_dir.name) / "properties.mmtf"
        sd = StructureData.init_from_file_name(working_mmtf_fn)
        random_data = list(range(256))
        encoded_random_data = mmtf_cppy.encodeRunLengthDeltaInt(list(range(256)))
        sd.atomProperties["256_atomColorList"] = random_data
        sd.atomProperties["256_atomColorList_encoded"] = encoded_random_data
        sd.write_to_file(tmp_output_fn)
        sd2 = StructureData.init_from_file_name(tmp_output_fn)
        assert sd2.atomProperties["256_atomColorList"] == random_data
        assert sd2.atomProperties["256_atomColorList_encoded"] == encoded_random_data
        assert (mmtf_cppy.decode_int32(sd2.atomProperties["256_atomColorList_encoded"]) == np.array(random_data)).all()

if __name__ == "__main__":
    unittest.main()
