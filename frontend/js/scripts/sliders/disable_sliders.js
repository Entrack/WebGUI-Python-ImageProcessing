function disable_sliders() {
	for (slider_i in slider_names) {
		$('#' + slider_names[slider_i]).slider('disable');
	}
}