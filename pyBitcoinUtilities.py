#
# pyBitcoinUtilites: Generate random, or from an input private key, Bitcoin public and private keys with QrCodes.
#					
# Author: Chiheb Nexus - 2017
# Credits:
#	Mastering Bitcoin
#	Link: http://chimera.labs.oreilly.com/books/1234000001802/ch04.html#_implementing_keys_and_addresses_in_python
# Licence: GPLv3
#

from src.bitcoinUtilities import BitcoinUtilities
from os import remove
from sys import version, exit

if int(version[0]) < 3:
	print("The minimal version to run this software is 'Python3.x'")
	exit()

try:
	import gi
	gi.require_version('Gtk', '3.0')
	from gi.repository import Gtk, GObject, GdkPixbuf

except ImportError:
	print("Error occurred. You need to install PyGi before running this software.")
	print("If you're running Ubuntu, try this command: ")
	print("sudo apt-get install python3-gi")
	exit()

try:
	import pyqrcode

except ImportError:
	print("Error occurred. You need to install pyqrcode before running this software.")
	print("If you're running Ubuntu, try this command: ")
	print("sudo apt-get install python3-pip")
	print("sudo pip install pyqrcode")
	import sys
	exit()


class PyBitcoinUtilities:
	def __init__(self):
		# Initialize BitcoinUtilites
		self.btc = BitcoinUtilities()

		# Gtk Builder
		self.builder = Gtk.Builder()
		self.builder.add_from_file("ui/interface.glade")

		# entry1: Bitcoin private key
		self.private_key_entry = self.builder.get_object("entry1")
		# entry2: Public address
		self.public_address_entry = self.builder.get_object("entry2")
		# entry3: Compressed private key
		self.compressed_private_key_entry = self.builder.get_object("entry3")
		# entry4: Compressed public address
		self.compressed_public_address_entry = self.builder.get_object("entry4") 

		# button1: Generate
		self.generate_button = self.builder.get_object("button1")
		self.generate_button.connect("clicked", self.generate_keys_addresses, 'random')
		#button2: Calculate
		self.calculate_button = self.builder.get_object("button2")
		self.calculate_button.connect("clicked", self.generate_keys_addresses, 'not random')

	def generate_keys_addresses(self, widget, msg):
		try:
			if msg == 'random':
				decoded_privkey = self.btc.get_priv_key('random')
				wif_privkey = self.btc.privkey_to_wif(decoded_privkey)
			else:
				wif_privkey = self.private_key_entry.get_text()
				decoded_privkey = self.btc.wif_to_priv(wif_privkey)

			compressed_privkey = self.btc.privkey_to_wif_compressed(decoded_privkey)
			public_key = self.btc.get_public_key_point(decoded_privkey)
			public_key_compressed = self.btc.compress_public_key(public_key)
			bitcoin_address = self.btc.generate_address(public_key)
			bitcoin_compressed_address = self.btc.generate_compress_address(public_key_compressed)

			self.private_key_entry.set_text(wif_privkey)
			path = self.set_qrcode(name = "private_key", key = wif_privkey)
			qr1 = self.builder.get_object("image1")
			qr1.set_from_file(path)

			self.compressed_private_key_entry.set_text(compressed_privkey)
			path = self.set_qrcode(name = "compressed_private_key", key = compressed_privkey)
			qr2 = self.builder.get_object("image3")
			qr2.set_from_file(path)

			self.public_address_entry.set_text(bitcoin_address)
			path = self.set_qrcode(name = "public_address_key", key = bitcoin_address)
			qr3 = self.builder.get_object("image2")
			qr3.set_from_file(path)

			self.compressed_public_address_entry.set_text(bitcoin_compressed_address)
			path = self.set_qrcode(name = "compressed_public_address_key", key = bitcoin_compressed_address)
			qr4 = self.builder.get_object("image4")
			qr4.set_from_file(path)

		except AssertionError:
			self.private_key_entry.set_text("Error occurred during the process. Please enter a valid private key.")
			self.compressed_public_address_entry.set_text("Error occurred during the process...")
			self.public_address_entry.set_text("Error occurred during the process...")
			self.compressed_private_key_entry.set_text("Error occurred during the process...")

		except TypeError:
			self.generate_keys_addresses(widget, 'random')

	def set_qrcode(self, name = "", key = ""):
		qr = pyqrcode.create(key)
		path = "/tmp/" + name + ".svg"
		# scale: set scale qr svg images
		# scale = 2: Small and fill into the window
		qr.svg(path , scale = 2)
		return path

	def delete_qr_images(self):
		# QR images paths
		qr_images = [
		"/tmp/compressed_private_key.svg",
		"/tmp/compressed_public_address_key.svg",
		"/tmp/private_key.svg",
		"/tmp/public_address_key.svg"
		]
		try:
			for k in qr_images:
				remove(k)
				print("'{0}' is removed".format(k))

		except FileNotFoundError:
			pass

	def main(self):
		# Get window object
		window = self.builder.get_object("window1")
		window.set_title("PyBitcoin keys utilities")
		pixbuf = GdkPixbuf.Pixbuf.new_from_file("ui/bitcoin.png")
		window.set_icon(pixbuf)
		#window.set_resizable(False)
		#window.set_default_size(900, 800)
		window.maximize()
		window.connect("delete-event", self.quit_app)
		window.show_all()

	def quit_app(self, widget, args):
		self.delete_qr_images()
		print("Safe exit...")
		Gtk.main_quit()

# Run the App
if __name__ == '__main__':
	GObject.threads_init()
	app = PyBitcoinUtilities()
	app.main()
	Gtk.main()

