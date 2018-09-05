function set_main_overlay_plots_disabled(state = true) {
	set_element_disabled('first_overlay_plot', state)
	set_element_disabled('first_overlay_plot_text', state)
	set_element_disabled('second_overlay_plot', state)
	set_element_disabled('second_overlay_plot_text', state)
	set_element_disabled('third_overlay_plot', state)
	set_element_disabled('third_overlay_plot_text', state)
}