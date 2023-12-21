import unittest
import mindhive.core_cortex as mh


class TestCore(unittest.TestCase):
    def test_core(self):
        self.assertIsNotNone(mh.ephemeral_init())
        self.assertIsNotNone(mh.persistent_init())


if __name__ == '__main__':
    unittest.main()
