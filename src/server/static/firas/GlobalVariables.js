var loadedData = null,
	sensorsColor = [],
	allDiffDates = [], //contains the different dates
	testFormat = d3.time.format("%Y-%m-%dT%H:%M:%S"),
	parseDate = d3.time.format("%Y-%m-%dT%H:%M:%S").parse, //shapes the date properly
	parsedDiffDates = [],
	formatTime = d3.time.format("%e %B"), //sets the time properly
	margin = {
		top: 50,
		right: 75,
		bottom: 50,
		left: 50
	},
	width = 1100 - margin.left - margin.right,
	height = 600 - margin.top - margin.bottom;

var xMin,
	xMax,
	yMin = 0,
	yMax = 0;

var tmp;

var myChart;
var x, y;

var h = 0; // color hue
var h2 = 0;

lines = false;



