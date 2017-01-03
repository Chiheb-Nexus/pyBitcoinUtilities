#
#	Base58 encode and decode utilities
#

from bExceptions import B58NotValid
import binascii

class b58:
	'''
		Encode & decode using base58 algorithm
	'''
	B58_DIGITS = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

	def encode(self, n = 0):
		res = []
		while n > 0:
			n, r = divmod(n, 58)
			res.append(b58.B58_DIGITS[r])

		res = ''.join(res[::-1])

		# Encode leading zeros as base58 zeros
		# In Python3 indexing a bytes returns numbers, not characters.
		czero = 0
		pad = 0
		for c in str(n):
			if c == czero: 
				pad += 1
			else: 
				break

		return b58.B58_DIGITS[0] * pad + res

	def decode(self, s = ""):
		'''
		Decode a base58-encoding string, returning bytes
		'''
		if not s:
			return b''

		# Convert the string to an integer
		n = 0
		for c in s:
			n *= 58
			if c not in b58.B58_DIGITS:
				raise B58NotValid(c)

			digit = b58.B58_DIGITS.index(c)
			n += digit

		# Convert the integer to bytes
		h = '%x' % n
		if len(h) % 2:
			h = '0' + h

		res = binascii.unhexlify(h.encode('utf8'))

		# Add padding back.
		pad = 0
		for c in s[:-1]:
			if c == b58.B58_DIGITS[0]: pad += 1
			else: 
				break

		return hex(int.from_bytes(b'\x00' * pad + res, byteorder = 'big'))