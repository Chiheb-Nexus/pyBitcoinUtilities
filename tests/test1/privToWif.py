# Credits: 
#	https://github.com/jgarzik/python-bitcoinlib/blob/master/bitcoin/base58.py
#	https://en.bitcoin.it/wiki/Wallet_import_format
#	http://bitcoin.stackexchange.com/questions/8057/how-do-i-get-the-public-bitcoin-address-from-a-given-private-key-in-wallet-impor
# 	https://en.bitcoin.it/wiki/List_of_address_prefixes

import hashlib, binascii
from b58EncodeDecode import b58
from bExceptions import ByteTypeNotValid

class PrivToWif:
	'''
		* Convert private address to WIF address
		* Convert WIF address to private address
		* Check if the converted addresses are equal
	'''

	def priv_to_wif(self, numpriv = "", b_type = '80'):
		'''
			* Convert private address to WIF address
			* Add byte at the beginning or at the end: 
				- 80 byte in the front of real private key to have a mainnet address
				- ef byte in front of private key to have a testnet address
				- 01 byte at the end of the private key to have a compressed one
		'''
		try:
			if b_type == 'ef' or b_type == '80':
				# zfill: adds 0 to the left to fill width which
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

			return b58.encode(self, step4)

		except ValueError as e:
			print("Error during processing data ...\n{0}".format(e))

		except TypeError as e:
			print("An odd error occured ...\n{0}".format(e))

	def wif_to_priv(self, wifpriv = ""):
		'''
			Convert WIF address to private address
		'''
		return b58.decode(self, wifpriv)[4:-8]

	def wif_check_sum(self, wifpriv = ""):
		'''
			Check if the converted addresses are equal by using their checksum
		'''
		encoded = b58.decode(self, wifpriv)

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

# Test
if __name__ == '__main__':
	app = PrivToWif()
	print(app.priv_to_wif("0x0C28FCA386C7A227600B2FE50B7CAE11EC86D3BF1FBE471BE89827E19D72AA1D", '80'))
	print(app.wif_to_priv("5HueCGU8rMjxEXxiPuD5BDku4MkFqeZyd4dZ1jvhTVqvbTLvyTJ"))
	print(app.wif_check_sum("5HueCGU8rMjxEXxiPuD5BDku4MkFqeZyd4dZ1jvhTVqvbTLvyTJ"))