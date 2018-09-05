$("#a_hist_button").click(function(){
	block_ui();
	check_if_ready("a_hist_button").then(() => {
		client.invoke("get_a_hist", get_selection_json(), (error, res) => {
			if (error) {
				console.error(error)
			} else {
				set_main_overlay_elements_disabled();
				set_element_disabled("first_overlay_plot", false);
				set_element_disabled("first_overlay_plot_text", false);
				$("#first_overlay_plot_text").text('A component histogram');

				plot_data("#first_overlay_plot", JSON.parse(res));

				open_main_overlay();
			}
		unblock_ui();
		})
	});
});