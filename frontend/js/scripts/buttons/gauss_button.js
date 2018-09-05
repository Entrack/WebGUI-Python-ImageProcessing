$("#gauss_button").click(function(){
	block_ui();
	check_if_ready("gauss_button").then(() => {
		sigma = $("#gauss_number")[0].value
		client.invoke("get_gaussian_filtered_image", sigma, (error, res) => {
			if (error) {
				console.error(error)
			} else {

				console.log(res)

				// set_main_overlay_elements_disabled(true);
				// set_main_overlay_images_disabled(false);

				// r_g_b_list = res.split(',');
				// set_image_from_base64("first_overlay_image", r_g_b_list[0]);
				// set_image_from_base64("second_overlay_image", r_g_b_list[1]);
				// set_image_from_base64("third_overlay_image", r_g_b_list[2]);
				// $("#first_overlay_image_text").text('Red component');
				// $("#second_overlay_image_text").text('Green component');
				// $("#third_overlay_image_text").text('Blue component');
				// open_main_overlay();
				
			}
		unblock_ui();
		})
	});
});