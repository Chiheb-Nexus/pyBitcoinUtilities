#
# pyBitcoinUtilites: Generate random, or from an input private key, Bitcoin public and private keys with QrCodes.
#					
# Author: Chiheb Nexus - 2017
# Credits:
#	Mastering Bitcoin
#	Link: http://chimera.labs.oreilly.com/books/1234000001802/ch04.html#_implementing_keys_and_addresses_in_python
# Licence: GPLv3
#

try:
	import bitcoin

except ImportError:
	print("Error occurred. You need to install bitcoin using pip before running this software.")
	print("If you're running Ubuntu, try this command: ")
	print("sudo apt-get install python3-pip")
	print("sudo pip install bitcoin")
	import sys
	sys.exit()

class BitcoinUtilities:

	def get_random_key(self):
		'''
			Get random dicimal key
			Hint: We can also use: os.urandom(32) then convert it into hex to generate random key
			Example: 
			import os, binascii
			binascii.hexlify(os.urandom(32))
		'''
		return bitcoin.random_key()

	def get_priv_key(self, privkey):
		'''
			Return Hex representation of a dicimal bitcoin private key
		'''
		if privkey == 'random':
			condition = True
			while condition:
				private_key = self.get_random_key()
				decoded_privkey = bitcoin.decode_privkey(private_key, 'hex')
				validation = 0 < decoded_privkey < bitcoin.N
				if validation:
					condition = False
					return decoded_privkey
		else:
			decoded_privkey = bitcoin.decoded_privkey(privkey, 'hex')
			validation = 0 < decoded_privkey < bitcoin.N
			if not validation:
				raise Exception("Key is not valid %r" % privkey)
			else:
				return decoded_privkey

	def privkey_to_wif(self, decoded_privkey):
		'''
			Return encoded WIF representation of a decoded private key (hex)
			Hint: * Add '80' byte at the beginning of the decoded private key to obtain a mainnet address
				  * Add 'ef' byte at the beginning of the decoded private key to optain a testnet address 
				  Then make double sha256 then return the base58 representation
		'''
		if decoded_privkey == 'random':
			return bitcoin.encode_privkey(self.get_priv_key('random'), 'wif')
		else:
			return bitcoin.encode_privkey(decoded_privkey, 'wif')

	def wif_to_priv(self, wifkey):
		'''
			Return the decoded private key from WIF key
		'''
		return bitcoin.decode_privkey(wifkey, 'wif')

	def get_priv_key_compressed(self, decoded_privkey):
		'''
			Return compressed private key.
			Hint: Add '01' byte at the end of the decoded private key (hex) to obtain a compressed address
				  Then make double sha256 
		'''
		if decoded_privkey == 'random':
			return self.get_priv_key('random') + int('01')
		else:
			return decoded_privkey + int('01')

	def privkey_to_wif_compressed(self, decoded_privkey):
		'''
			Return compressed private key
			Hint: After adding '01' byte at the end of the decoded private key (hex)
				  And make double sha256. Finally return the base58 representation
		'''
		if decoded_privkey == 'random':
			compressed = self.get_priv_key_compressed('random')
			return bitcoin.encode_privkey(compressed, 'wif')
		else:
			compressed = decoded_privkey + int('01')
			return bitcoin.encode_privkey(compressed, 'wif')

	def get_public_key_point(self, decoded_privkey):
		'''
			Return Bitcoin public key point
		'''
		return bitcoin.fast_multiply(bitcoin.G, decoded_privkey)

	def encode_public_key(self, decoded_privkey):
		'''
			Return a tuple of the encoded Bitcoin public key 
		'''
		return bitcoin.encode_pubkey(self.get_public_key_point(decoded_privkey), 'hex')

	def compress_public_key(self, pubkey):
		'''
			Compress the bitcoin public key
		'''
		public_key_x, public_key_y = pubkey
		if (public_key_y % 2) == 0:
			compressed_prefix = '02'
		else:
			compressed_prefix = '03'

		return compressed_prefix + bitcoin.encode(public_key_x, 16)

	def generate_address(self, pubkey):
		'''
			Generate a Bitcoin address
		'''
		return bitcoin.pubkey_to_address(pubkey)

	def generate_compress_address(self, compressed_pubkey):
		'''
			Generate a compressed Bitcoin address
		'''
		return bitcoin.pubkey_to_address(compressed_pubkey)

	def return_random_bitcoin_address(self):
		'''
			Return random Bitcoin: Public & Private keys
			Output: dict{public_key, private_key}
		'''
		decoded_privkey = self.get_priv_key('random')
		priv_to_wif = self.privkey_to_wif(decoded_privkey)
		public_key = self.get_public_key_point(decoded_privkey)
		return {"public_key": self.generate_address(public_key), "private_key": priv_to_wif}

	def return_pubkey_from_privkey(self, privkey):
		'''
			Return Public key from a private keyr
			Output: dict{public_key, private_key}
		'''
		decoded_privkey = self.wif_to_priv(privkey)
		public_key = self.get_public_key_point(decoded_privkey)
		return {"public_key": self.generate_address(public_key), "private_key": privkey}

	def return_random_compressed_bitcoin_address(self):
		'''
			Return random compressed Public & private keys
			Output: dict{public_key_compressed, private_key_compressed}
		'''
		decoded_privkey = self.get_priv_key('random')
		priv_key_compressed = self.privkey_to_wif_compressed(decoded_privkey)
		public_key_point = self.get_public_key_point(decoded_privkey)

		return {"public_key_compressed": self.generate_address(public_key_point), 
		"private_key_compressed":priv_key_compressed}
