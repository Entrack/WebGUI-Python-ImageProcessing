function set_image_from_base64(image_id, base64) {
	document.getElementById(image_id).src = 'data:image/jpg;base64,' + base64.toString();
}