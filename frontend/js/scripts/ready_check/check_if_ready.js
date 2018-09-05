if_check = false

timeouts = {
	'rgb_matrix_button' : 2000,
	'gauss_button' : 1000
}

function check_if_ready(action) {
	time_out = 0
	if (if_check) {
		if (action in timeouts) {
			time_out = timeouts[action]
		}
	}
	return new Promise((resolve) => setTimeout(resolve, time_out));
}