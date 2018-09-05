import numpy as np

class ImageProcessor():
	def __init__(self):
		self.np_rgb_im = None
		
		print(self.__class__.__name__, 'inited!')

	def fill_in_rgb_from_pil(self, pil_image):
		self.np_rgb_im = np.asarray(pil_rgb_im, dtype = np.float32) 

	def get_np_image_by_area(self, image, area = None):
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

	# def get_cropped_pil_image(self, pil_image, scaled_area):
	# 	return pil_image.crop((scaled_area['x1'], scaled_area['y1'], 
	# 			scaled_area['x2'], scaled_area['y2']))

	#
	# ALGORYTHMS
	#  

	def rgb2hsv_pixel(self, r, g, b):
		r, g, b = r/255.0, g/255.0, b/255.0
		mx = max(r, g, b)
		mn = min(r, g, b)
		df = mx-mn
		if mx == mn:
			h = 0
		elif mx == r:
			h = (60 * ((g-b)/df) + 360) % 360
		elif mx == g:
			h = (60 * ((b-r)/df) + 120) % 360
		elif mx == b:
			h = (60 * ((r-g)/df) + 240) % 360
		if mx == 0:
			s = 0
		else:
			s = df/mx
		v = mx
		return h, s, v

	def x_to_x_np(operation, np_rgb_im):
		hsv_im = np.zeros(np_rgb_im.shape)
		for row in hsv_im:
			for column in row:
				hsv_im[row, column] = operation(np_rgb_im[row, column])
		return hsv_im

	def rgb2lab_pixel(inputColor):
		num = 0
		RGB = [0, 0, 0]
		for value in inputColor :
			 value = float(value) / 255
			 if value > 0.04045 :
				  value = ( ( value + 0.055 ) / 1.055 ) ** 2.4
			 else :
				  value = value / 12.92
			 RGB[num] = value * 100
			 num = num + 1
		XYZ = [0, 0, 0,]
		X = RGB [0] * 0.4124 + RGB [1] * 0.3576 + RGB [2] * 0.1805
		Y = RGB [0] * 0.2126 + RGB [1] * 0.7152 + RGB [2] * 0.0722
		Z = RGB [0] * 0.0193 + RGB [1] * 0.1192 + RGB [2] * 0.9505
		XYZ[ 0 ] = round( X, 4 )
		XYZ[ 1 ] = round( Y, 4 )
		XYZ[ 2 ] = round( Z, 4 )
		XYZ[ 0 ] = float( XYZ[ 0 ] ) / 95.047
		XYZ[ 1 ] = float( XYZ[ 1 ] ) / 100.0
		XYZ[ 2 ] = float( XYZ[ 2 ] ) / 108.883
		num = 0
		for value in XYZ :
			 if value > 0.008856 :
				  value = value ** ( 0.3333333333333333 )
			 else :
				  value = ( 7.787 * value ) + ( 16 / 116 )
			 XYZ[num] = value
			 num = num + 1
		Lab = [0, 0, 0]
		L = ( 116 * XYZ[ 1 ] ) - 16
		a = 500 * ( XYZ[ 0 ] - XYZ[ 1 ] )
		b = 200 * ( XYZ[ 1 ] - XYZ[ 2 ] )
		Lab [ 0 ] = round( L, 4 )
		Lab [ 1 ] = round( a, 4 )
		Lab [ 2 ] = round( b, 4 )
		return Lab

	#
	# CALLABLE FUNCTIONS START HERE
	#  

	def get_rgb_components_grayscale_images(self, area):
		r_array = self.get_np_image_by_area(self.np_rgb_im, area)
		r_array[:, :, 1] = r_array[:, :, 0]
		r_array[:, :, 2] = r_array[:, :, 0]
		
		g_array = self.get_np_from_pil_by_area(self.np_rgb_im, area)
		g_array[:, :, 0] = g_array[:, :, 1]
		g_array[:, :, 2] = g_array[:, :, 1]

		b_array = self.get_np_from_pil_by_area(self.np_rgb_im, area)
		b_array[:, :, 0] = b_array[:, :, 2]
		b_array[:, :, 1] = b_array[:, :, 2]

		return r_array, g_array, b_array

	def get_hsv_components_grayscale_images(self, area):
		hsv_im = self.x_to_x_np(self.rgb2hsv_pixel, self.np_rgb_im)

		h_array = self.get_np_image_by_area(hsv_im, area)
		h_array[:, :, 1] = h_array[:, :, 0]
		h_array[:, :, 2] = h_array[:, :, 0]
		
		s_array = self.get_np_image_by_area(hsv_im, area)
		s_array[:, :, 0] = s_array[:, :, 1]
		s_array[:, :, 2] = s_array[:, :, 1]

		v_array = self.get_np_image_by_area(hsv_im, area)
		v_array[:, :, 0] = v_array[:, :, 2]
		v_array[:, :, 1] = v_array[:, :, 2]

		return h_array, s_array, v_array

	def get_lab_components_grayscale_images(self, area):
		lab_im = self.x_to_x_np(self.rgb2lab_pixel, self.np_rgb_im)

		l_array = self.get_np_image_by_area(lab_im, area)
		l_array[:, :, 1] = l_array[:, :, 0]
		l_array[:, :, 2] = l_array[:, :, 0]
		self.scale_np_array(l_array, 100, 255)
		
		a_array = self.get_np_image_by_area(lab_im, area)
		a_array[:, :, 0] = a_array[:, :, 1]
		a_array[:, :, 2] = a_array[:, :, 1]
		self.scale_np_array(a_array, 100, 255)

		b_array = self.get_np_image_by_area(lab_im, area)
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

	def get_lab_hist(self, area):
		lab_np_im = self.x_to_x_np(self.rgb2lab_pixel, self.np_rgb_im)

		lab_pil_im = Image.fromarray(lab_np_im)
		if not self.if_area_empty(area):
			scaled_area = self.get_image_scaled_area(lab_pil_im, area)
			lab_pil_im = self.get_cropped_pil_image(lab_pil_im, scaled_area)
		return lab_pil_im.histogram()

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