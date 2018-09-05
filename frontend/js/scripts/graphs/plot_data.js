function plot_data(graph_name, data, steps = true) {
	$.plot(graph_name, [{
		data: data,
		lines: { show: true, steps: steps}
	}]);
}