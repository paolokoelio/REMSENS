function DesignLowerChart() {


	//---------------Design the lower chart SVG and borders---------------
	navWidth = width;
	navHeight = 180 - margin.top - margin.bottom;


	navXScale = d3.time.scale()
		.domain([xMin, xMax])
		.range([0, navWidth]);
	navYScale = d3.scale.linear()
		.domain([yMin, yMax])
		.range([navHeight, 0]);

	navXAxis = d3.svg.axis()
		.scale(navXScale)
		.orient('bottom');

	viewport = d3.svg.brush()
		.x(navXScale)
		.on("brush", function() {
			x.domain(viewport.empty() ? navXScale.domain() : viewport.extent());
			redrawChart();
		});

	navChart = d3.select("#chart").append('svg')
		.classed('navigator', true)
		.attr('width', navWidth + margin.left + margin.right)
		.attr('height', navHeight + margin.top + margin.bottom)
		.append('g')
		.attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

	navChart.append("g")
		.attr("class", "viewport")
		.call(viewport)
		.selectAll("rect")
		.attr("height", navHeight);

	navChart.append('g')
		.attr('class', 'x axis')
		.attr('transform', 'translate(0,' + navHeight + ')')
		.call(navXAxis);

	navChart.append("g")
		.attr("class", "viewport")
		.call(viewport)
		.selectAll("rect")
		.attr("height", navHeight);
	//------------------------------------------------------------------------------------------

	//---------------function to redraw chart when zoomed---------------
	function redrawChart() {
		if (lines) {
			DrawVoronoi();
			for (var i = 0; i < loadedData.sensors.length; i++) {
				myChart.selectAll("#value" + i).attr("d", valueline(loadedData.sensors[i].collectedData));
			}
			//myChart.selectAll(".voronoi").attr("d", voronoi(validMappingSensors));
		}
		myChart.select('.x.axis').call(xAxis);
	}
	//------------------------------------------------------------------------------------------
}