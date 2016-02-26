function fixDates() {

	//---------------add parsed dates element to the sensors---------------
	for (var i = 0; i < loadedData.sensors.length; ++i) {
		for (var j = 0; j < loadedData.sensors[i].collectedData.length; j++) {
			loadedData.sensors[i].collectedData[j].parsedDate = parseDate(loadedData.sensors[i].collectedData[j].date);
		}
	}
	//------------------------------------------------------------------------------------------

	//---------------create and array of the different dates and order it and sets min and max of x axis---------------
	for (var i = 0; i < loadedData.sensors.length; i++) {
		for (var j = 0; j < loadedData.sensors[i].collectedData.length; j++) {
			if (allDiffDates.indexOf(loadedData.sensors[i].collectedData[j].date) == -1) {
				allDiffDates.push(loadedData.sensors[i].collectedData[j].date);
			}
		}
	}
	allDiffDates = allDiffDates.sort();

	for (var i = 0; i < allDiffDates.length; i++) {
		parsedDiffDates.push(parseDate(allDiffDates[i]));
	}

	xMin = parsedDiffDates[0];
	xMax = parsedDiffDates[parsedDiffDates.length - 1];
}
//------------------------------------------------------------------------------------------


function minANDmax() {
	tmp = 0;
	//---------------set min and max of y axis---------------
	for (var i = 0; i < loadedData.sensors.length; i++) {
		for (var j = 0; j < loadedData.sensors[i].collectedData.length; j++) {
			if (loadedData.sensors[i].collectedData[j].value >= tmp) {
				yMax = loadedData.sensors[i].collectedData[j].value;
				tmp = yMax;
			}
		}
	}

	tmp = 0;
	for (var i = 0; i < loadedData.sensors.length; i++) {
		for (var j = 0; j < loadedData.sensors[i].collectedData.length; j++) {
			if (loadedData.sensors[i].collectedData[j].value <= tmp) {
				yMin = loadedData.sensors[i].collectedData[j].value;
				tmp = yMin;
			}
		}
	}
}
//------------------------------------------------------------------------------------------