function CreateSensors() {

//---------------Generate a different color for each sensor---------------
    for (var i = 0; i < loadedData.sensors.length; i++) {
        sensorsColor.push(d3.hsl(h, .53, .53).toString());
        h = h + 10;
        if (h >= 350) {
            h2 += 3;
            h = h2;
            if (h2 >= 350) {
                h2 = 7;
                h = h2
            }
        }
    }
//------------------------------------------------------------------------------------------


//---------------Create a checkbox for each sensor---------------
    for (var i = 0; i < loadedData.sensors.length; i++) {
        var newCheckBox = document.createElement('input');
        newCheckBox.setAttribute("class", "checkbox" + i);
        newCheckBox.setAttribute("type", "checkbox");
        newCheckBox.setAttribute("name", loadedData.sensors[i].sensorName);
        newCheckBox.setAttribute("id", "sensor" + i);
        //newCheckBox.addEventListener('click', DrawLines(i));

        var label = document.createElement('label');
        label.appendChild(document.createTextNode("Sensor " + loadedData.sensors[i].sensorName));
        label.setAttribute("style", "color: " + sensorsColor[i]);

        var newLine = document.createElement("br");

        document.getElementById("checkboxes").appendChild(newCheckBox);
        document.getElementById("checkboxes").appendChild(label);
        document.getElementById("checkboxes").appendChild(newLine);
    }
}

//------------------------------------------------------------------------------------------