$("#b_hist_button").click(function(){
	block_ui();
	check_if_ready("b_hist_button").then(() => {
		client.invoke("get_b_hist", get_selection_json(), (error, res) => {
			if (error) {
				console.error(error)
			} else {
				set_main_overlay_elements_disabled();
				set_element_disabled("first_overlay_plot", false);
				set_element_disabled("first_overlay_plot_text", false);
				$("#first_overlay_plot_text").text('B component histogram');

				plot_data("#first_overlay_plot", JSON.parse(res));

				open_main_overlay();
			}
		unblock_ui();
		})
	});
});