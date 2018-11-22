'''
Author: Brian Chen
Created for CSEC
Seminar on Continuous Integration: csec.club/seminars
01/11/2018
'''

import unittest
from palindromes import (is_palindrome, safe_open, count_palindromes)


class TestIsPalindrome(unittest.TestCase):
	

	def test_BasicPalindrome1(self):
		self.assertTrue(is_palindrome("aba"))


	def test_BasicPalindrome2(self):
		self.assertTrue(is_palindrome("*.4a4n5n4a4.*"))


	def test_BasicPalindrome3(self):
		self.assertTrue(is_palindrome("So|163361|Os"))


	def test_CaseResistance1(self):
		self.assertTrue(is_palindrome("SaAs"))


	def test_CaseResitance2(self):
	
		self.assertTrue(is_palindrome("Se0Es"))

	def test_NonPalindrome1(self):
		self.assertFalse(is_palindrome("Soze"))


	def test_NonPalindrome2(self):
		self.assertFalse(is_palindrome("ZoE.,EoZ"))


	def test_EmptyPalindrome(self):
		self.assertTrue(is_palindrome(""))


	def test_OneLetterPalindrome(self):
		self.assertTrue(is_palindrome("W"))


class TestSafeOpen(unittest.TestCase):
	

	def setUp(self):
		self.exist_file = 'tests/test1'
		self.nonexist_file = 'test'


	def test_OpenExistingFile(self):
		f = safe_open(self.exist_file)
		self.assertTrue(f is not None)


	def test_OpenNonexistingFile(self):
		f = safe_open(self.nonexist_file)
		self.assertEqual(f, None)

class TestCountPalindromes(unittest.TestCase):
	

	def setUp(self):
		self.file_without_palindromes = safe_open("tests/test2")
		self.file_with_palindromes = safe_open("tests/test1")


	def test_FileWithoutPalindromes(self):
		self.assertEqual(count_palindromes(self.file_without_palindromes), 0)


	def test_FileWithPalindromes(self):
		self.assertEqual(count_palindromes(self.file_with_palindromes), 4)


if __name__ == '__main__':
	unittest.main()