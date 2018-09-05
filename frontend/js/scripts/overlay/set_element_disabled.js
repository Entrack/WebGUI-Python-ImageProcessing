function set_element_disabled(name, state = true) {
	if (state) {
		state = "none"
	} else {
		state = "block"
	}
	document.getElementById(name).style.display = state;
}