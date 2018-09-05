from __future__ import print_function
from real_app_initer.RealAppIniter import RealAppIniter

class AppAPI(object):
	def __init__(self, ip, port):
		real_app_initer = RealAppIniter(ip, port)
		self.real_app = real_app_initer.get_real_app()
		print('AppAPI', 'inited!')
	
	def safe_call(self, function, *args):
		try:
			return function(*args)
		except Exception as e:
			return e

	def echo(self, text):
		return text

	#
	# API STARTS HERE
	#  

	def load_image_from_file(self, filepath):
		return self.safe_call(self.real_app.load_image_from_file,
			filepath)

	def get_rgb_components_grayscale_images(self, selection):
		return self.safe_call(self.real_app.get_rgb_components_grayscale_images,
			selection)

	def get_hsv_components_grayscale_images(self, selection):
		return self.safe_call(self.real_app.get_hsv_components_grayscale_images, 
			selection)

	def get_lab_components_grayscale_images(self, selection):
		return self.safe_call(self.real_app.get_lab_components_grayscale_images, 
			selection)

	def get_l_hist(self, selection):
		return self.safe_call(self.real_app.get_l_hist, 
			selection)

	def get_a_hist(self, selection):
		return self.safe_call(self.real_app.get_a_hist, 
			selection)

	def get_b_hist(self, selection):
		return self.safe_call(self.real_app.get_b_hist, 
			selection)

	def get_changed_hue_image(self, hue):
		return self.safe_call(self.real_app.get_changed_hue_image, 
			hue)

	def get_changed_saturation_image(self, saturation):
		return self.safe_call(self.real_app.get_changed_saturation_image, 
			saturation)

	def get_changed_value_image(self, value):
		return self.safe_call(self.real_app.get_changed_value_image, 
			value)

	def get_gaussian_filtered_image(self, sigma):
		return self.safe_call(self.real_app.get_gaussian_filtered_image, 
			sigma)




















