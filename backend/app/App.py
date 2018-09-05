from __future__ import print_function

from app.image_processing.ImageProcessor import ImageProcessor as ip

import time
from PIL import Image
import numpy as np
from io import BytesIO
import base64
import codecs, json 
#import pathlib2 as pathlib
# import hashlib


class App():
	def __init__(self, client):
		self.client = client
		self.update_time = 1.0

		self.ip = ip()
		self.jpeg_transfer_quality = 70

		print('App inited!')

	def run(self):
		while True:
			self.update()

	def update(self):
		self.do()
		time.sleep(self.update_time)

	def do(self):
		# print('do')
		# self.client.update_event()
		# print(self.md5('backend/image_processor/ImageProcessor.py'))
		return

	def md5(self, file_name):
		hash_md5 = hashlib.md5()
		with open(file_name, "rb") as f:
			for chunk in iter(lambda: f.read(4096), b""):
				hash_md5.update(chunk)
		return hash_md5.hexdigest()

	def open_pil_image(self, filepath):
		return Image.open(filepath)

	def get_current_rgb_image(self):
		return self.rgb_to_base64(self.ip.get_current_rgb_im())

	def rgb_to_base64(self, rgb_image):
		byte_image = self.rgb_to_bytesio(rgb_image)
		return base64.b64encode(byte_image.getvalue())       
		
	def rgb_to_bytesio(self, rgb_image):
		im = Image.fromarray(np.uint8(rgb_image))
		buffered = BytesIO()
		# im = im.convert("RGB")
		im.save(buffered, format="JPEG", quality=self.jpeg_transfer_quality)
		return buffered

	def to_json(self, obj):
		return json.dumps(obj)

	def numpy_to_json(self, array):
		return self.to_json(array.tolist())

	def np_rgbs_list_to_string(self, p_rgbs_list):
		list_string = ""
		for picture in p_rgbs_list:
			list_string += str(self.rgb_to_base64(picture))[2:-1] + ','
		return list_string[0:-1]

	def get_np_x_for_hist(self, hist, x_range = None):
		x_ticks = 0
		if x_range is None:
			x_ticks = np.arange(len(hist))
		else:
			x_ticks = np.linspace(x_range[0], x_range[1], len(hist))
		return np.array((x_ticks, hist)).transpose()

	#
	# CALLABLE FUNCTIONS START HERE
	#  

	def load_image_from_file(self, filepath):
		self.ip.set_pil_image(self.open_pil_image(filepath))
		return self.get_current_rgb_image()

	def get_rgb_components_grayscale_images(self, selection):
		selection_dict = json.loads(selection)
		rgb_components_grayscale_images = self.ip.get_rgb_components_grayscale_images(selection_dict)
		return self.np_rgbs_list_to_string(rgb_components_grayscale_images)

	def get_hsv_components_grayscale_images(self, selection):
		selection_dict = json.loads(selection)
		hsv_components_grayscale_images = self.ip.get_hsv_components_grayscale_images(selection_dict)
		return self.np_rgbs_list_to_string(hsv_components_grayscale_images)

	def get_lab_components_grayscale_images(self, selection):
		selection_dict = json.loads(selection)
		lab_components_grayscale_images = self.ip.get_lab_components_grayscale_images(selection_dict)
		return self.np_rgbs_list_to_string(lab_components_grayscale_images)

	def get_l_hist(self, selection):
		selection_dict = json.loads(selection)
		hist = self.ip.get_l_hist(selection_dict)
		x_and_hist = self.get_np_x_for_hist(hist, [0, 100])
		return self.numpy_to_json(x_and_hist)

	def get_a_hist(self, selection):
		selection_dict = json.loads(selection)
		hist = self.ip.get_a_hist(selection_dict)
		x_and_hist = self.get_np_x_for_hist(hist, [-128, 127])
		return self.numpy_to_json(x_and_hist)

	def get_b_hist(self, selection):
		selection_dict = json.loads(selection)
		hist = self.ip.get_b_hist(selection_dict)
		x_and_hist = self.get_np_x_for_hist(hist, [-128, 127])
		return self.numpy_to_json(x_and_hist)

	def get_changed_hue_image(self, hue):
		return self.ip.get_changed_hue_image(hue)

	def get_changed_saturation_image(self, saturation):
		return self.ip.get_changed_saturation_image(saturation)

	def get_changed_value_image(self, value):
		return self.ip.get_changed_value_image(value)

	def get_gaussian_filtered_image(self, sigma):
		return self.ip.get_gaussian_filtered_image(sigma)





















	# return str(self.rgb_to_base64(self.ip.get_rgb_grayscale_images()))[2:-1]
	# return self.rgb_to_base64(self.ip.get_rgb_grayscale_images())

	# return str(self.rgb_to_base64(self.ip.get_rgb_grayscale_images()))[2:-1]

	# Old server-client tests
	# def do(self):
	#     print('do')

	#     # Calls update_event function on frontend server
	#     self.client.update_event()

	#     # Calls empty function on frontend server
	#     # self.client.empty()

	#     # Calls with_reply function on frontend server
	#     # and writes the response to file (enable import pathlib)
	#     # reply = self.client.with_reply('Chen')
	#     # file = open('sc_test.txt', 'w')
	#     # file.write(str(reply))          
	#     # file.close()

	# Get image from fs
	# def get_image(self, path):
	#     with open("path", "rb") as image_file:
	#         encoded_string = base64.b64encode(image_file.read())
	#         return encoded_string

	# Out to source
	# I = np.divide(I, 0.8, out=I)

	# Json dump
	# def get_table(self, arg):
	#     a = np.arange(10).reshape(5,2)
	#     b = a.tolist()
	#     return json.dumps(b)
	#     return json.dumps([[0, 0], [1, 1], [2, 2], [3, 3]])