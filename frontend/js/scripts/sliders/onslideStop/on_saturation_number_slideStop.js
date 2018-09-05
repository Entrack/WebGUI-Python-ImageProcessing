$("#saturation_number").on("slideStop", function(slideEvt) {
	client.invoke("get_changed_saturation_image", slideEvt.value, (error, res) => {
		if (error) {
			console.error(error)
		} else {
			console.log(res)
		}
	})
});