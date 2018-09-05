function show_main_image_selection() {
	main_image_imgAreaSelect.setOptions({hide: false});
	if (main_image_imgAreaSelect.getSelection().height != 0) {
		main_image_imgAreaSelect.setOptions({show: true});
	}
	main_image_imgAreaSelect.update();
}