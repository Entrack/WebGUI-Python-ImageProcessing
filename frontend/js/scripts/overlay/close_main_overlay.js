function close_main_overlay() {
	show_main_image_selection();
	enable_sliders();

	set_main_overlay_elements_disabled(true);
	document.getElementById("main_overlay").style.width = "0%";
}