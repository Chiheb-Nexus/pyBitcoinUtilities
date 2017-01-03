import hashlib, binascii

def encode_b58(n):
	b58_digits = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
	res = []
	while n > 0:
		n, r = divmod (n, 58)
		res.append(b58_digits[r])

	res = ''.join(res[::-1])

	# Encode leading zeros as base58 zeros
	# In Python3 indexing a bytes returns numbers, not characters.
	czero = 0

	pad = 0
	for c in str(n):
		if c == czero: pad += 1
		else: break

	return b58_digits[0] * pad + res

def numtowif(numpriv):
	try:
		step1 = '80'+hex(int(numpriv, 16))[2:].strip('L').zfill(64)
		step2 = hashlib.sha256(binascii.unhexlify(step1)).hexdigest()
		step3 = hashlib.sha256(binascii.unhexlify(step2)).hexdigest()
		step4 = int(step1 + step3[:8] , 16)

		return encode_b58(step4)

	except ValueError as e:
		print("Error during processing data ...\n{0}".format(e))
	except TypeError as e:
		print("An odd error occured ...\n{0}".format(e))

def decode_b58(s):
	b58_digits = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
	"""Decode a base58-encoding string, returning bytes"""
	if not s:
		return b''

	# Convert the string to an integer

	n = 0
	for c in s:
		n *= 58
		if c not in b58_digits:
			raise Exception('Character %r is not a valid base58 character' % c)
		digit = b58_digits.index(c)
		n += digit

	# Convert the integer to bytes
	h = '%x' % n
	if len(h) % 2:
		h = '0' + h
	res = binascii.unhexlify(h.encode('utf8'))

	# Add padding back.
	pad = 0
	for c in s[:-1]:
		if c == b58_digits[0]: pad += 1
		else: break

	return b'\x00' * pad + res

def wiftonum(wifpriv):
	return hex(int.from_bytes(decode_b58(wifpriv), byteorder='big'))[4:-8]

def validwif(wifpriv):
	return numtowif(wiftonum(wifpriv))==wifpriv

print(numtowif('0x0C28FCA386C7A227600B2FE50B7CAE11EC86D3BF1FBE471BE89827E19D72AA1D'))
print(wiftonum('5HueCGU8rMjxEXxiPuD5BDku4MkFqeZyd4dZ1jvhTVqvbTLvyTJ'))
#print(validwif('5HueCGU8rMjxEXxiPuD5BDku4MkFqeZyd4dZ1jvhTVqvbTLvyTJ'))
#print(validwif('5HueCGU8rMjxEXxiPuD5BDku4MkFqeZyd4dZ1jvhTVqvbTLvyTK'))