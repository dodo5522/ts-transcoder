#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from manememo import Manememo

class TestManememo(unittest.TestCase):
	def test_init(self):
		objManememo = Manememo()
		self.assertIsInstance(objManememo, Manememo, None)
		pass

if __name__ == '__main__':
	unittest.main()

