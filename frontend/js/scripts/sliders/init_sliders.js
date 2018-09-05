slider_names = [
'hue_number',
'saturation_number',
'value_number'
]

function init_sliders() {
	for (slider_i in slider_names) {
		$('#' + slider_names[slider_i]).slider({
			formatter: function(value) {
				return value;
			}
		});	
	}
}

$(document).ready(function () {					
	init_sliders();
});