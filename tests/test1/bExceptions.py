#
#	Custom exceptions
#

class B58NotValid(Exception):
	def __init__(self, c):
		Exception.__init__(self, 'Character %r is not a valid base58 character' % c)

class ByteTypeNotValid(Exception):
	def __init__(self, b_type):
		Exception.__init__(self, "Character %r is not a valid Byte" % b_type)