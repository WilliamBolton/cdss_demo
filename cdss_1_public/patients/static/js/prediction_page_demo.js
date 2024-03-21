document.addEventListener('DOMContentLoaded', function () {
    // Access the variables defined in the HTML file

    // Function to update text based on the patient's name
    function updateText() {
        // Condition based on the patient's name
        if (patientName === "Patient 3" || patientName === "Patient 7" || patientName === "Patient 8" || patientName === "Patient 9" || patientName === "Patient 10" || patientName === "Patient 11" || patientName === "Patient 12") {
        document.getElementById("figureTitle").innerHTML = "Table displaying similar patients features for comparison <br> and indicating feature contribution towards the predictions";
        } else {
        document.getElementById("figureTitle").innerHTML = "Heatmap indicating feature similarity between <br> this patient and the similar patients";
        }
    }

    // Call the function when the page loads
    window.onload = updateText;

    // Display CSV data in the tables
    displayCsvData(patientDataJson, "patient-table");
    displayCsvData(similarDataJson, "similar-table");

    // Function to display JSON data in the table
    function displayCsvData(jsonData, string) {
        const table = document.getElementById(string);

        // Clear the table first to avoid appending to existing data
        table.innerHTML = "";

        // Add table header
        const headerRow = document.createElement("tr");
        Object.keys(jsonData[0]).forEach(column => {
            const th = document.createElement("th");
            th.textContent = column;
            headerRow.appendChild(th);
        });
        table.appendChild(headerRow);

        // Add table rows
        jsonData.forEach(dataRow => {
            const row = document.createElement("tr");
            Object.entries(dataRow).forEach(([key, value]) => {
                const td = document.createElement("td");
                td.textContent = value;
                // console.log(`Cell: ${key}, Value: ${value}`);

                
                // Apply conditional class based on column name and value
                if (key === 'AI CDSS prediction' || key === 'Real action' || key === 'AI CDSS prediction (higher threshold)') {
                    const colorClass = getColorClass(value);
                    // console.log(`Cell: ${key}, Value: ${value}, Color Class: ${colorClass}`);
                    if (colorClass) {
                        td.classList.add(colorClass);
                    }
                    td.classList.add(getColorClass(value));
                }

                if (key === 'Prediction correct' || key === 'Higher threshold prediction correct') {
                    const colorClass = getColorClass2(value);
                    // console.log(`Cell: ${key}, Value: ${value}, Color Class: ${colorClass}`);
                    if (colorClass) {
                        td.classList.add(colorClass);
                    }
                    td.classList.add(getColorClass(value));
                }
                
                row.appendChild(td);
            });
            table.appendChild(row);
        });
    }

    // Function to determine the appropriate class based on the value
    function getColorClass(value) {
        const lowercaseValue = value.toLowerCase();  // Convert to lowercase for case-insensitive comparison
        const isSwitch = lowercaseValue === 'switch' || lowercaseValue === 'switched';
    
        if (isSwitch) {
            return 'bg-success-light';  // Green for Switch or Switched
        } else if (lowercaseValue === 'dont switch' || lowercaseValue === 'didnt switch') {
            return 'bg-danger-light';  // Red for Dont switch or Didnt switch
        } else {
            return 'default-class';  // Default class if no match
        }
    }

    function getColorClass2(value) {
        const colorClass = value === 'Yes' ? 'bg-success-bright' : (value === 'No' ? 'bg-danger-bright' : 'default-class');
        return colorClass;
    }

    // Function to get CSRF token from cookies
    function getCSRFToken() {
        var name = 'csrftoken';
        var value = "; " + document.cookie;
        var parts = value.split("; " + name + "=");
        if (parts.length === 2) {
            return parts.pop().split(";").shift();
        }
        return null;
    }

    // Log CSRF token
    var csrf_token = getCSRFToken();
    console.log('CSRF token from template:', csrf_token);

});