import sys
import unittest
from unittest.mock import patch
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import supervise_c6_30ms_shared as sup


class SharedCapacityTests(unittest.TestCase):
    def test_busy_gpus_can_share_and_largest_free_is_selected(self):
        states = [(46068, 16000, [10]), (46068, 17480, [11]), (46068, 12000, [12]), (46068, 9000, [13])]
        with patch.object(sup, "gpu_state", side_effect=lambda gpu: states[gpu]):
            self.assertEqual(sup.choose_gpu(), (1, 17480, [11]))

    def test_low_capacity_is_rejected_even_without_other_pids(self):
        with patch.object(sup, "gpu_state", return_value=(46068, 8191, [])):
            self.assertIsNone(sup.choose_gpu())


if __name__ == "__main__":
    unittest.main()
