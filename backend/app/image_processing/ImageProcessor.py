import numpy as np
from PIL import Image
from PIL import ImageFilter

from skimage import io, color

class ImageProcessor():
	def __init__(self):
		self.do_make_thumbnail = False
		self.thumbnail_max_size = 640, 640

		self.pil_rgb_im = None
		# self.np_rgb_im = None
		
		print(self.__class__.__name__, 'inited!')

	def make_thumbnail_if_needed(self):
		if self.do_make_thumbnail:
			self.make_thumbnail()

	def make_thumbnail(self):
		self.pil_rgb_im.thumbnail(self.thumbnail_max_size, Image.ANTIALIAS)

	def fill_in_rgb_from_pil(self):
		self.np_rgb_im = np.asarray(self.pil_rgb_im, dtype = np.float32) 

	def get_np_from_pil_by_area(self, pil_image, area = None):
		np_im = np.array(pil_image)
		if not self.if_area_empty(area):
			np_im = self.get_np_by_area(np_im, area)
		return np_im

	def if_area_empty(self, area):
		is_empty = False
		if not area is None:
			if area['width'] is 0 or area['height'] is 0:
				is_empty = True
		else:
			is_empty = True
		return is_empty

	def get_np_by_area(self, np_im, area):
		scaled_area = self.get_image_scaled_area(np_im, area)
		return np_im[scaled_area['y1']:scaled_area['y2'], scaled_area['x1']:scaled_area['x2'], :]

	def get_image_scaled_area(self, im, area):
		scaled_area = {}
		if type(im) is np.ndarray:
			height = im.shape[0]
			width = im.shape[1]
		if type(im) is Image.Image:
			height = im.size[0]
			width = im.size[1]

		scaled_area['x1'] = int(area['x1'] * width)
		scaled_area['x2'] = int(area['x2'] * width)
		scaled_area['y1'] = int(area['y1'] * height)
		scaled_area['y2'] = int(area['y2'] * height)
		scaled_area['width'] = int(area['width'] * width)
		scaled_area['height'] = int(area['height'] * height)

		return scaled_area

	def scale_np_array(self, np_array, initial_max, resulting_max):
		np.multiply(np_array, resulting_max / initial_max,
			out=np_array, casting="unsafe")
		return np_array

	def get_cropped_pil_image(self, pil_image, scaled_area):
		return pil_image.crop((scaled_area['x1'], scaled_area['y1'], 
				scaled_area['x2'], scaled_area['y2']))

	def get_lab_hist(self, area):
		# Possible optimization
		if not self.if_area_empty(area):
			np_rgb_im = np.array(self.pil_rgb_im)
			lab_np_im = color.rgb2lab(self.get_np_by_area(np_rgb_im, area))
		else:
			lab_np_im = color.rgb2lab(self.pil_rgb_im)

		# lab_np_im = color.rgb2lab(self.pil_rgb_im)

		lab_pil_im = Image.fromarray(lab_np_im, "LAB")
		if not self.if_area_empty(area):
			scaled_area = self.get_image_scaled_area(lab_pil_im, area)
			lab_pil_im = self.get_cropped_pil_image(lab_pil_im, scaled_area)
		return lab_pil_im.histogram()

	#
	# CALLABLE FUNCTIONS START HERE
	#  

	def set_pil_image(self, pil_image):
		self.pil_rgb_im = pil_image
		self.pil_rgb_im = self.pil_rgb_im.convert("RGB")
		self.make_thumbnail_if_needed()

	def get_current_rgb_im(self):
		self.fill_in_rgb_from_pil()
		return self.np_rgb_im

	def get_rgb_components_grayscale_images(self, area):
		r_array = self.get_np_from_pil_by_area(self.pil_rgb_im, area)
		r_array[:, :, 1] = r_array[:, :, 0]
		r_array[:, :, 2] = r_array[:, :, 0]
		
		g_array = self.get_np_from_pil_by_area(self.pil_rgb_im, area)
		g_array[:, :, 0] = g_array[:, :, 1]
		g_array[:, :, 2] = g_array[:, :, 1]

		b_array = self.get_np_from_pil_by_area(self.pil_rgb_im, area)
		b_array[:, :, 0] = b_array[:, :, 2]
		b_array[:, :, 1] = b_array[:, :, 2]

		return r_array, g_array, b_array

	def get_hsv_components_grayscale_images(self, area):
		# Possible optimization
		# if not self.if_area_empty(area):
		# 	scaled_area = self.get_image_scaled_area(self.pil_rgb_im, area)
		# 	im = self.get_cropped_pil_image(self.pil_rgb_im, scaled_area)
		# else:
		# 	im = self.pil_rgb_im

		hsv_im = self.pil_rgb_im.convert('HSV')

		h_array = self.get_np_from_pil_by_area(hsv_im, area)
		h_array[:, :, 1] = h_array[:, :, 0]
		h_array[:, :, 2] = h_array[:, :, 0]
		
		s_array = self.get_np_from_pil_by_area(hsv_im, area)
		s_array[:, :, 0] = s_array[:, :, 1]
		s_array[:, :, 2] = s_array[:, :, 1]

		v_array = self.get_np_from_pil_by_area(hsv_im, area)
		v_array[:, :, 0] = v_array[:, :, 2]
		v_array[:, :, 1] = v_array[:, :, 2]

		return h_array, s_array, v_array

	def get_lab_components_grayscale_images(self, area):
		lab_im = color.rgb2lab(self.pil_rgb_im)

		l_array = self.get_np_from_pil_by_area(lab_im, area)
		l_array[:, :, 1] = l_array[:, :, 0]
		l_array[:, :, 2] = l_array[:, :, 0]
		self.scale_np_array(l_array, 100, 255)
		
		a_array = self.get_np_from_pil_by_area(lab_im, area)
		a_array[:, :, 0] = a_array[:, :, 1]
		a_array[:, :, 2] = a_array[:, :, 1]
		self.scale_np_array(a_array, 100, 255)

		b_array = self.get_np_from_pil_by_area(lab_im, area)
		b_array[:, :, 0] = b_array[:, :, 2]
		b_array[:, :, 1] = b_array[:, :, 2]
		self.scale_np_array(b_array, 100, 255)

		return l_array, a_array, b_array

	def get_l_hist(self, area):
		lab_hist = self.get_lab_hist(area)
		return lab_hist[0:256]

	def get_a_hist(self, area):
		lab_hist = self.get_lab_hist(area)
		return lab_hist[256:512]

	def get_b_hist(self, area):
		lab_hist = self.get_lab_hist(area)
		return lab_hist[512:768]		

	def get_changed_hue_image(self, hue):
		return 'get_changed_hue_image'

	def get_changed_saturation_image(self, saturation):
		return 'get_changed_saturation_image'

	def get_changed_value_image(self, value):
		return 'get_changed_value_image'

	def get_gaussian_filtered_image(self, sigma):
		return 'get_gaussian_filtered_image'































		# self.pil_rgb_im = self.pil_rgb_im.filter(ImageFilter.GaussianBlur(radius=50))
		# # self.pil_rgb_im = self.pil_rgb_im.convert("L")
		# self.fill_in_rgb_from_pil()
		# for i in range(256):
		# 	for j in range(256):
		# 		self.np_rgb_im[i,j] = (0, 0, 0)
		# return self.np_rgb_im, self.np_rgb_im, self.np_rgb_im

		# r_array = np.zeros([self.np_rgb_im.shape[0], self.np_rgb_im.shape[1], 3])
		# r_array[:, :, 0] = self.np_rgb_im[:, :, 2]
		# r_array[:, :, 1] = self.np_rgb_im[:, :, 2]
		# r_array[:, :, 2] = self.np_rgb_im[:, :, 2]
		# self.np_rgb_im = r_array

		# # self.fill_in_rgb_from_pil()

		# return self.np_rgb_im, self.np_rgb_im, self.np_rgb_im

		# r_component = self.pil_rgb_im.copy()