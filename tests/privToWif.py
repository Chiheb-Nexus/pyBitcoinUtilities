# Credits: 
#	https://github.com/jgarzik/python-bitcoinlib/blob/master/bitcoin/base58.py
#	https://en.bitcoin.it/wiki/Wallet_import_format
#	http://bitcoin.stackexchange.com/questions/8057/how-do-i-get-the-public-bitcoin-address-from-a-given-private-key-in-wallet-impor
# 	https://en.bitcoin.it/wiki/List_of_address_prefixes

import hashlib, binascii

class B58NotValid(Exception):
	def __init__(self, c):
		Exception.__init__(self, 'Character %r is not a valid base58 character' % c)

class ByteTypeNotValid(Exception):
	def __init__(self, b_type):
		Exception.__init__(self, "Character %r is not a valid Byte" % b_type)

class PrivToWif:
	def __init__(self):
		self.b58_digits = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

	def encode_b58(self, n = 0):
		res = []
		while n > 0:
			n, r = divmod (n, 58)
			res.append(self.b58_digits[r])

		res = ''.join(res[::-1])

		# Encode leading zeros as base58 zeros
		# In Python3 indexing a bytes returns numbers, not characters.
		czero = 0
		pad = 0
		for c in str(n):
			if c == czero: pad += 1
			else: 
				break

		return self.b58_digits[0] * pad + res

	def decode_b58(self, s = ""):
		"""Decode a base58-encoding string, returning bytes"""
		if not s:
			return b''

		# Convert the string to an integer
		n = 0
		for c in s:
			n *= 58
			if c not in self.b58_digits:
				raise B58NotValid(c)

			digit = self.b58_digits.index(c)
			n += digit

		# Convert the integer to bytes
		h = '%x' % n
		if len(h) % 2:
			h = '0' + h

		res = binascii.unhexlify(h.encode('utf8'))

		# Add padding back.
		pad = 0
		for c in s[:-1]:
			if c == self.b58_digits[0]: pad += 1
			else: 
				break

		return b'\x00' * pad + res

	def priv_to_wif(self, numpriv = "", b_type = '80'):
			try:
				
				if b_type == 'ef' or b_type == '80':
					# zfill: adds 0 to the left to fill width which
					# add byte at the beginning or at the end: 
					# 	80 byte in the front of real private key to have a mainnet address
					# 	ef byte in front of private key to have a testnet address
					# 	01 byte at the end of the private key to have a compressed one
					step1 = b_type + hex(int(numpriv, 16))[2:].strip('L').zfill(64)

				elif b_type == '01':
					step1 = hex(int(numpriv, 16))[2:].strip('L').zfill(64) + b_type
				else:
					raise ByteTypeNotValid(b_type)

				# step2: first sha256 hash
				step2 = hashlib.sha256(binascii.unhexlify(step1)).hexdigest()
				# step3: second sha256 hash
				step3 = hashlib.sha256(binascii.unhexlify(step2)).hexdigest()
				# step4: step1 + first 4 bytes from step3 converted all to int (hex -> int)
				step4 = int(step1 + step3[:8] , 16)
				return self.encode_b58(step4)

			except ValueError as e:
				print("Error during processing data ...\n{0}".format(e))
			
			except TypeError as e:
				print("An odd error occured ...\n{0}".format(e))

	def wif_to_priv(self, wifpriv = ""):
		return hex(int.from_bytes(self.decode_b58(wifpriv), byteorder = 'big'))[4:-8]

	def wif_check_sum(self, wifpriv = ""):
			encoded = hex(int.from_bytes(self.decode_b58(wifpriv), byteorder = 'big'))
			# FIXME: Not the best way but did the job
			#
			# first: fisrt part from the base58 converted byte
			# last: checksum
			first, last = encoded[2:-8], encoded[len(encoded)-1:len(encoded)-9:-1][::-1]
			# first sha256 hash
			a = hashlib.sha256(binascii.unhexlify(first)).hexdigest()
			# second sha256 hash
			b = hashlib.sha256(binascii.unhexlify(a)).hexdigest()

			# test if the first 4 bytes are equal to las which is the checksum
			if b[:8] == last:
				return True
			else:
				return False

			

if __name__ == '__main__':
	app = PrivToWif()
	print(app.priv_to_wif("0x0C28FCA386C7A227600B2FE50B7CAE11EC86D3BF1FBE471BE89827E19D72AA1D", '80'))
	print(app.wif_to_priv("5HueCGU8rMjxEXxiPuD5BDku4MkFqeZyd4dZ1jvhTVqvbTLvyTJ"))
	print(app.wif_check_sum("5HueCGU8rMjxEXxiPuD5BDku4MkFqeZyd4dZ1jvhTVqvbTLvyTJ"))