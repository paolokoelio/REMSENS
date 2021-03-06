

d3.json("Library/data.json", function(error, data) {
        
    

    loadedData = data;

       
        
    //---------------Control if file is correct---------------
    if (data && data.sensors.length > 0) {

    } else {
        window.alert("ERROR! File is empty");
    }

    //---------------Create senors and colors---------------
    CreateSensors();
    //------------------------------------------------------------------------------------------

    //---------------Set and parse dates, mins and max---------------    
    fixDates();
    minANDmax();
    //------------------------------------------------------------------------------------------

    //---------------Create an array of objects to use with voronoi function---------------
    datesoes = [];
    arrayOfObjects = [];

    for (var i = 0; i < data.sensors.length; i++) {
        datesoes[i] = new Array();
        sensori = {
            name: loadedData.sensors[i].sensorName,
            values: []
        };
        for (var j = 0; j < loadedData.sensors[i].collectedData.length; j++) {
            datesoes[i].push(loadedData.sensors[i].collectedData[j].parsedDate);

            sensori.values[j] = {
                sensori: sensori,
                date: datesoes[i][j],
                value: (loadedData.sensors[i].collectedData[j].value),
                mU: (loadedData.sensors[i].measurementUnit),
                color: sensorsColor[i]
            }
        };
        arrayOfObjects.push(sensori);
    };
    //------------------------------------------------------------------------------------------

    //---------------Set behavior of checkboxes on change---------------
    document.addEventListener("change", DrawLines, false);
    //------------------------------------------------------------------------------------------

    //---------------Design Charts---------------
    DesignChart();
    DesignLowerChart();
    //------------------------------------------------------------------------------------------

});
