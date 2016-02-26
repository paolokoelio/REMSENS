function Drawing(i) {

	for (var k = 0; k < loadedData.sensors.length; k++) {
		if ($('input.checkbox' + k).is(':checked')) {
			lines = true;
			break;
		} else lines = false;
	}

	//---------------Assign data to respective path--------------- 
	valueline = d3.svg.line()
		.x(function(d) {
			return x(d.parsedDate);
		})
		.y(function(d) {
			return y(d.value);
		})

	//---------------Design the path---------------
	plotArea.append("path")
		.attr("class", "line")
		.attr("d", valueline(loadedData.sensors[i].collectedData))
		.attr("id", "value" + i)
		.style("stroke", sensorsColor[i]) // color of the line
		.style("stroke-width", 1.2)
		.style("stroke-linejoin", "round");

}

function DrawVoronoi() {
	d3.select("#chart").selectAll(".voronoi").remove();
	validMappingSensors = [];

	//Add checked sensors to design voronoi map
	for (var i = 0; i < loadedData.sensors.length; i++) {
		if ($('input.checkbox' + i).is(':checked')) {
			validMappingSensors.push(arrayOfObjects[i]);
		}
	}

	//---------------Assign data to respective path--------------- 
	voronoi = d3.geom.voronoi()
		.x(function(d) {
			return x(d.date);
		})
		.y(function(d) {
			return y(d.value);
		})
		/*.clipExtent([
			[-margin.left, -margin.top],
			[width + margin.right, height + margin.bottom]
		])*/;


	voronoiGroup = plotArea.append("g")
		.attr("class", "voronoi");


	voronoiGroup.selectAll("path")
		.data(voronoi(d3.nest()
			.key(function(d) {
				return x(d.date) + "," + y(d.value);
			})
			.rollup(function(v) {
				return v[0];
			})
			.entries(d3.merge(validMappingSensors.map(function(d) {
				return d.values;
			})))
			.map(function(d) {
				return d.values;
			})))
		.enter().append("path")
		.attr("d", function(d) {
			return "M" + d.join("L") + "Z";
		})
		.datum(function(d) {
			return d.point;
		})
		.on("mouseover", mouseover)
		.on("mouseout", mouseout);


	function mouseover(d) {
		//d3.select("#value" + i).classed("city--hover", true);
		//d.sensori.valueline.parentNode.appendChild(d.sensori.valueline);
		focus.attr("transform", "translate(" + x(d.date) + "," + y(d.value) + ")");
		focus.select("text").text(d.sensori.name + "-" + d.value + "" + d.mU)
			.attr("fill", d.color);
		focus.select("circle").attr('fill', d.color);
	}

	function mouseout(d) {
		d3.select("#value" + i).classed("city--hover", false);
		focus.attr("transform", "translate(-100,-100)");
	};

}

function DrawingLower(i) {
	var i = +i;

	navLine = d3.svg.line()
		.x(function(d) {
			return navXScale(d.parsedDate);
		})
		.y(function(d) {
			return navYScale(d.value);
		});

	navChart.append('path')
		.attr('d', navLine(loadedData.sensors[i].collectedData))
		.attr("id", "lower" + i)
		.style("stroke", sensorsColor[i]);
}



function DrawLines(e) {
	if (e.target.type == "checkbox") {
		var i = e.target.id.substring(6);
		if (e.target.checked) {
			Drawing(i);
			DrawingLower(i);
		} else {
			d3.select("#chart").selectAll("#value" + i).remove();
			d3.select("#chart").selectAll("#lower" + i).remove();
		}
		DrawVoronoi();
	}
}