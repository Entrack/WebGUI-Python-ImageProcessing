$("#rgb_matrix_button").click(function(){
	block_ui();
	check_if_ready("rgb_matrix_button").then(() => {
		client.invoke("get_rgb_components_grayscale_images", get_selection_json(), (error, res) => {
			if (error) {
				console.error(error)
			} else {

				set_main_overlay_elements_disabled(true);
				set_main_overlay_images_disabled(false);

				r_g_b_list = res.split(',');
				set_image_from_base64("first_overlay_image", r_g_b_list[0]);
				set_image_from_base64("second_overlay_image", r_g_b_list[1]);
				set_image_from_base64("third_overlay_image", r_g_b_list[2]);
				$("#first_overlay_image_text").text('Red component');
				$("#second_overlay_image_text").text('Green component');
				$("#third_overlay_image_text").text('Blue component');
				open_main_overlay();
				
			}
		unblock_ui();
		})
	});
});