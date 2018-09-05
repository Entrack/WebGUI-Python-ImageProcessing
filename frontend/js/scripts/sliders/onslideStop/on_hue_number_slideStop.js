$("#hue_number").on("slideStop", function(slideEvt) {
	client.invoke("get_changed_hue_image", slideEvt.value, (error, res) => {
		if (error) {
			console.error(error)
		} else {
			console.log(res)
		}
	})
});