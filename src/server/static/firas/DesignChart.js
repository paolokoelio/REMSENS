function DesignChart() {
	$("svg").css({
		top: 78,
		position: 'absolute'
	});

	x = d3.time.scale()
		.range([0, width])
		.domain([xMin, xMax]);
	y = d3.scale.linear()
		.range([height, 0])
		.domain([yMin, yMax]).nice();


	yAxis = d3.svg.axis()
		.scale(y)
		.orient("left")
		.tickValues([yMin, yMin + (yMax - yMin) / 5, yMin + 2 * (yMax - yMin) / 5, yMin + 3 * (yMax - yMin) / 5, yMin + 4 * (yMax - yMin) / 5, yMax]);

	xAxis = d3.svg.axis()
		.scale(x)
		.ticks(5)
		.tickFormat(d3.time.format("%m-%Y"));


	myChart = d3.select('#chart').classed('chart', true).append('svg')
		.attr('width', width + margin.left + margin.right)
		.attr('height', height + margin.top + margin.bottom)
		.append('g')
		.attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

	plotArea = myChart.append('g')
		.attr('clip-path', 'url(#plotAreaClip)');

	plotArea.append('clipPath')
		.attr('id', 'plotAreaClip')
		.append('rect')
		.attr({
			width: width,
			height: height
		});


	$("#chart").css({
		top: 80,
		left: 70,
		position: 'absolute'
	});

	//Adding Grid lines
	function make_y_axis() {
		return d3.svg.axis()
			.scale(y)
			.orient("left")
			.tickValues([yMin, yMin + (yMax - yMin) / 5, yMin + 2 * (yMax - yMin) / 5, yMin + 3 * (yMax - yMin) / 5, yMin + 4 * (yMax - yMin) / 5, yMax]);
	};
	//Draw the lines
	myChart.append("g")
		.attr("class", "grid")
		.call(make_y_axis()
			.tickSize(-width, 0, 0)
			.tickFormat("")
		);

	myChart.append("g")
		.attr("class", "y axis")
		.call(yAxis);

	myChart.append("g")
		.attr("class", "x axis")
		.attr("transform", "translate(0," + height + ")")
		.call(xAxis);


	myChart.append("text") // text label for the x axis 
		.attr("transform",
			"translate(" + (width + margin.right * 1 / 3) + " ," +
			(height) + ")")
		.style("text-anchor", "middle")
		.text("Data");

	myChart.append("text")
		.attr("transform", "rotate(-90)") //rotates the axes
		.attr("y", -margin.left)
		.attr("x", 0 - (height / 2))
		.attr("dy", "1em")
		.style("text-anchor", "middle")
		.text("Valore");

	focus = myChart.append("g")
		.attr("transform", "translate(-100,-100)")
		.attr("class", "focus");


	focus.append("circle")
		.attr("r", 3.5);

	focus.append("text")
		.attr("y", -10);

}