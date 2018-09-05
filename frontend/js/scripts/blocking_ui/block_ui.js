loading_gifs = [
'chen_quetioned',
'chen_running', 
'chensaw', 
'chen_and_ran'
]

function block_ui() {
	gif_name = loading_gifs[Math.floor(Math.random() * loading_gifs.length)]
	$.blockUI({ message: '<img src="frontend/images/' + gif_name + '.gif" style="max-width: 300px;"/>' });
}