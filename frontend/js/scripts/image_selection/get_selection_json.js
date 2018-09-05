function get_selection_json() {
	selection = main_image_imgAreaSelect.getSelection()

	width = $('#main_image').width()
	height = $('#main_image').height()

	try {
		selection['x1'] /= width
		selection['x2'] /= width
		selection['y1'] /= height
		selection['y2'] /= height
		selection['width'] /= width
		selection['height'] /= height
	} catch (err) {console.log('get_selection_json:', err)}

	return JSON.stringify(selection);
}