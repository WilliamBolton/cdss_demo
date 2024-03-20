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

    // Post other js
    //document.addEventListener('DOMContentLoaded', function () {
        
        // Track hovering

        // Variables to track hover start time
        const patient_table = document.getElementById('patient-table');
        const similar_table = document.getElementById('similar-table');
        const image = document.getElementById('feature-image');
        const positivePoints = document.querySelectorAll('.positive-point');
        const negativePoints = document.querySelectorAll('.negative-point');
        
        let hoverStartTime;

        // Attach event listeners to the entire patient_table for hover events
        patient_table.addEventListener('mouseover', function (event) {
            hoverStartTime = new Date().getTime();
        });
        console.log('Hover - patient_table');

        patient_table.addEventListener('mouseout', function (event) {
            const hoverEndTime = new Date().getTime();
            const hoverDuration = (hoverEndTime - hoverStartTime) / 1000; // Convert to seconds

            // Extract relevant information for recording
            const component = 'patient_table';

            // Send AJAX request to the server
            sendHoverEvent(component, hoverDuration);
        });

        // Attach event listeners to each row in similar patients table for hover events
        const rows = Array.from(similar_table.getElementsByTagName('tr'));
        console.log('rows:', rows)
        rows.forEach(row => {
            // console.log('row:', row)
            row.addEventListener('mouseover', function (event) {
                hoverStartTime = new Date().getTime();
            });
            console.log('Hover - similar_table');

            row.addEventListener('mouseout', function (event) {
                const hoverEndTime = new Date().getTime();
                const hoverDuration = (hoverEndTime - hoverStartTime) / 1000; // Convert to seconds

                // Extract relevant information for recording
                const component = `similar_table_${row.cells[0].textContent}`; // Updated metric with prefix

                // Send AJAX request to the server
                sendHoverEvent(component, hoverDuration);
            });
        });

        // Attach event listeners to the feature-image for hover events
        image.addEventListener('mouseover', function (event) {
            hoverStartTime = new Date().getTime();
        });
        console.log('Hover - image');
        image.addEventListener('mouseout', function (event) {
            const hoverEndTime = new Date().getTime();
            const hoverDuration = (hoverEndTime - hoverStartTime) / 1000; // Convert to seconds

            // Extract relevant information for recording
            const component = 'feature_image';

            // Send AJAX request to the server
            sendHoverEvent(component, hoverDuration);
        });

        // Attach event listeners to the LLM positive points for hover events
        positivePoints.forEach(point => {
            point.addEventListener('mouseover', function (event) {
                hoverStartTime = new Date().getTime();
            });
            console.log('Hover - positivePoints');
            point.addEventListener('mouseout', function (event) {
                const hoverEndTime = new Date().getTime();
                const hoverDuration = (hoverEndTime - hoverStartTime) / 1000; // Convert to seconds

                // Extract relevant information for recording
                const component = 'LLM_positive_points';

                // Send AJAX request to the server
                sendHoverEvent(component, hoverDuration);
            });
        });

        // Attach event listeners to the LLM negative points for hover events
        negativePoints.forEach(point => {
            point.addEventListener('mouseover', function (event) {
                hoverStartTime = new Date().getTime();
            });
            console.log('Hover - negativePoints');
            point.addEventListener('mouseout', function (event) {
                const hoverEndTime = new Date().getTime();
                const hoverDuration = (hoverEndTime - hoverStartTime) / 1000; // Convert to seconds

                // Extract relevant information for recording
                const component = 'LLM_negative_points';

                // Send AJAX request to the server
                sendHoverEvent(component, hoverDuration);
            });
        });

        function sendHoverEvent(component, hoverDuration) {
            const xhr = new XMLHttpRequest();
            xhr.open('POST', '/record_hover_event/');
            xhr.setRequestHeader('Content-Type', 'application/json');

            // Include CSRF token in headers
            const csrfToken = getCSRFToken();
            if (csrfToken) {
                xhr.setRequestHeader('Content-Type', 'application/json');
                xhr.setRequestHeader('X-CSRFToken', csrfToken);
                // Set the X-Requested-With header
                xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

                // Get patient_id
                var patientNameElement = document.getElementById('patientName');
                // console.log('patientNameElement', patientNameElement)

                if (patientNameElement) {
                    var patientName = patientNameElement.getAttribute('data-name');
                    // console.log('Patient Name:', patientName);
    
                    xhr.onload = function () {
                        if (xhr.status === 200) {
                            console.log('Hover event recorded successfully');
                        }
                    };
                    // console.log('component:', component);
                    // console.log('We are here!');
                    xhr.send(JSON.stringify({ component: component, hover_duration: hoverDuration, patientId: patientName }));
                }
            }
        };

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