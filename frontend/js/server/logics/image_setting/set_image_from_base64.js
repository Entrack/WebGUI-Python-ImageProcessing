function set_image_from_base64(container, base64, format = 'png'){
	console.log('set_image_from_base64');
	container.src = 'data:image/' + format + ';base64,' + base64.toString();
}