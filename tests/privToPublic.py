#
# Credit:
#	http://bitcoin.stackexchange.com/questions/37040/ripemd160sha256publickey-where-am-i-going-wrong
#	https://davanum.wordpress.com/2014/03/17/generating-a-bitcoin-private-key-and-address/
#

import ecdsa
import binascii
import hashlib
from b58EncodeDecode import b58

class PrivToPublic:

	def priv_to_public_key(self, key_byte = b''):
		sk = ecdsa.SigningKey.from_string(key_byte, curve = ecdsa.SECP256k1)
		return binascii.hexlify(b'\04' + sk.verifying_key.to_string()).decode("utf8")

	def public_to_priv_key(self, pub_key):
		s = hashlib.new('sha256', pub_key.encode()).digest()
		f = hashlib.new('ripemd160', s).digest()
		return b58.encode(self, binascii.hexlify(f).decode("utf8"))
		




# Test
if __name__ == '__main__':
	app = PrivToPublic()
	import os
	key_byte = os.urandom(32)
	#print(key_byte)
	a = app.priv_to_public_key(key_byte)
	print("priv_to_public_key: ", a)
	print("public_to_priv_key: ", app.public_to_priv_key(a))

