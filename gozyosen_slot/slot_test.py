import unittest
from unittest import mock
import gozyosen_slot

class SlotTest(unittest.TestCase):
    def setUp(self):
        self.marks = ['a', 'b', 'c', 'd', 'e', 'f',]
        pass

    def tearDown(self):
        pass

    @mock.patch('random.randint')
    def test_get_slot(self, randint_mock=mock.Mock):
        randint_mock.side_effect = [1, 2, 3, 4]
        result = gozyosen_slot.get_slot_result(self.marks, 10, 3)
        self.assertEqual(['c', 'c', 'c'], result)

        randint_mock.side_effect = [2, 0, 1, 2]
        result = gozyosen_slot.get_slot_result(self.marks, 10, 3)
        self.assertEqual(['a', 'b', 'c'], result)

        randint_mock.side_effect = [2, 2, 2, 2, 2, 2, 2, 1]
        result = gozyosen_slot.get_slot_result(self.marks, 10, 3)
        self.assertEqual(['c', 'c', 'b'], result)

        randint_mock.side_effect = [1, 4, 3, 2, 1]
        result = gozyosen_slot.get_slot_result(self.marks, 10, 3)
        self.assertEqual(['e', 'e', 'e'], result)

        randint_mock.side_effect = [1, 4, 3, 2, 1]
        result = gozyosen_slot.get_slot_result(self.marks, 10, 3)
        self.assertEqual(['e', 'e', 'e'], result)

        randint_mock.side_effect = [10, 4, 3, 2, 1]
        result = gozyosen_slot.get_slot_result(self.marks, 10, 3)
        self.assertEqual(['e', 'd', 'c'], result)


if __name__ == '__main__':
    unittest.main()
