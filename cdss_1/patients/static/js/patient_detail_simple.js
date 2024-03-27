 document.addEventListener('DOMContentLoaded', function () {
    // Access the variables defined in the HTML file
    // vitalsDataJson and vitalsDataNoNanJson are now available here
    
    let timePoints = []; // Declare timePoints globally
    let metrics = []; // Declare metrics globally

    // Display CSV data in the table
    displayCsvData(vitalsDataNoNanJson);

    // Function to display JSON data in the table
    function displayCsvData(jsonData) {
        const table = document.getElementById("vitals-table");

        // Extract metrics and time data
        metrics = jsonData.map(item => item["Metric / Time (hours)"]);
        timePoints = Object.keys(jsonData[0]).filter(key => key !== "Metric / Time (hours)");

        // Add table header
        const headerRow = document.createElement("tr");
        const th = document.createElement("th");
        th.textContent = "Metric / Time (hours)";
        headerRow.appendChild(th);
        timePoints.forEach(timePoint => {
            const th = document.createElement("th");
            th.textContent = timePoint;
            headerRow.appendChild(th);
        });
        table.appendChild(headerRow);

        // Add table rows
        metrics.forEach(metric => {
            const row = document.createElement("tr");
            const td = document.createElement("td");
            td.textContent = metric;
            row.appendChild(td);

            timePoints.forEach(timePoint => {
                const td = document.createElement("td");
                td.textContent = jsonData.find(item => item["Metric / Time (hours)"] === metric)[timePoint];
                row.appendChild(td);
            });

            table.appendChild(row);
        });

        // Update ECharts options after displaying CSV data
        updateEChartsOptions();
    }

    // Function to update ECharts options
    function updateEChartsOptions() {
        // Set custom colors for the series
        const customColors = ['#5470C6', '#91CC75', '#EE6666', '#EECBAD', '#ADADAD', '#F4E001', '#0FAEAF', '#FF69B4', '#6B8E23', '#FFA500', '#BA55D3'];

        // Declare options object
        const options = {
            title: {
                text: ''
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: [], // Initialize legend data
                selected: {}, // Empty initially, indicating all series are visible
            },
            color: customColors, // Use custom colors
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: timePoints,
            },
            yAxis: {
                type: 'value',
            },
            series: [], // Initialize series data
            dataZoom: [
                {
                    type: 'inside',
                    start: 0,
                    end: 100,
                },
                {
                    show: true,
                    type: 'slider',
                    start: 0,
                    end: 100,
                    yAxisIndex: [0],
                    width: '2%'
                },
                {
                    show: true,
                    type: 'slider',
                    start: 0,
                    end: 100,
                    xAxisIndex: [0],
                    height: '2%',
                    bottom: 5
                },
            ],
        };

        // Add series data and update legend data
        metrics.forEach(metric => {
            // Skip metrics with specific names
            if (metric !== 'Conscious Level' && metric !== 'Supplemental Oxygen') {
                options.series.push({
                    name: metric,
                    type: 'line',
                    data: timePoints.map(timePoint => {
                        const item = vitalsDataJson.find(item => item["Metric / Time (hours)"] === metric);
                        return item ? item[timePoint] : null;
                    }),
                    connectNulls: true // Connects points with missingness
                });
                // Add metric to legend data
                options.legend.data.push(metric);
            }
        });

        // Initialize ECharts
        const echartsContainer = document.getElementById('echarts-container');
        const echartsInstance = echarts.init(echartsContainer);

        // Set the options
        echartsInstance.setOption(options);

        // Echarts legend click event listener
        echartsInstance.on('legendselectchanged', function (params) {
            // Toggle visibility of selected series based on legend selection
            Object.keys(options.legend.selected).forEach(seriesName => {
                options.legend.selected[seriesName] = params.selected[seriesName];
            });

            // Update chart with new legend settings
            echartsInstance.setOption(options);
        });
        
        function logLegendClick(legendName, timestamp) {
            // Get the patient - ie., second last character of the webpage URL
            const patient = window.location.href.slice(-2, -1);

            // Prepare data to send to Django
            const data = {
                legendName: legendName,
                patient: patient,
                timestamp: timestamp
            };
                
            // Send the data to Django using AJAX
            fetch('/save_legend_click/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken() // Make sure to set this variable with the CSRF token
                },
                body: JSON.stringify(data)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to send legend click data to Django');
                }
                return response.json();
            })
            .then(data => {
                console.log('Legend click data successfully sent to Django:', data);
            })
            .catch(error => {
                console.error('Error sending legend click data to Django:', error);
            });
        }  

        // Echarts legend click event listener
        echartsInstance.on('legendselectchanged', function (params) {
            // Toggle visibility of selected series based on legend selection
            Object.keys(options.legend.selected).forEach(seriesName => {
                options.legend.selected[seriesName] = params.selected[seriesName];
            });

            // Update chart with new legend settings
            echartsInstance.setOption(options);

            // Log legend click
            const legendName = params.name; // Get the name of the clicked legend
            const timestamp = new Date().toISOString(); // Get the current timestamp
            logLegendClick(legendName, timestamp);
        });
    }

    // User form
    document.getElementById('userInputForm').addEventListener('submit', function(event) {
    const dropdown = document.getElementById('switch_choice');
    if (dropdown.value === "") {
        // If the dropdown option is not selected, prevent the form submission
        dropdown.setCustomValidity("Please select an option from the dropdown.");
        event.preventDefault();
    } else {
        // If the dropdown option is selected, remove the custom validity
        dropdown.setCustomValidity("");
    }
    });

    // Post other js
    // document.addEventListener('DOMContentLoaded', function () {
        
        // Click tracker

        // Function to send AJAX request
        function trackLinkClick(linkId) {
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/track_link_click/');

            // Include CSRF token in headers
            var csrfToken = getCSRFToken();        
            if (csrfToken) {
                xhr.setRequestHeader('Content-Type', 'application/json');
                xhr.setRequestHeader('X-CSRFToken', csrfToken);
                // Set the X-Requested-With header
                xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

                // Get patient_id
                var patientNameElement = document.getElementById('patientName');
                console.log('patientNameElement', patientNameElement)

                if (patientNameElement) {
                    var patientName = patientNameElement.getAttribute('data-name');
                    console.log('Patient Name:', patientName);

                    xhr.onload = function () {
                        if (xhr.status === 200) {
                            console.log('Link click recorded successfully');
                        }
                    };

                    // console.log('We are here!');
                    xhr.send(JSON.stringify({ linkId: linkId, patientId: patientName }));
                }
            }
        }

        // Add event listener for 'guidelines' link
        var guidelinesLink_simple = document.getElementById('guidelinesLink_simple');
        // console.log('guidelinedetailsLink');
        guidelinesLink_simple.addEventListener('click', function () {
            trackLinkClick('guidelinesLink_simple');
        });
        
        // Track hovering

        // Variables to track hover start time
        const table = document.getElementById('vitals-table');
        const plot = document.getElementById('echarts-container');
        const card = document.querySelector('.card');
        const guidelinesEmbed = document.querySelector('embed[src*="Final_IV_to_Oral_Switch_Decision_Aid_based_on_NationalCriteria_UKHSA.pdf"]');
        
        let hoverStartTime;

        /*// Attach event listeners to the entire table for hover events
        table.addEventListener('mouseover', function (event) {
            hoverStartTime = new Date().getTime();
        });
        console.log('table');
        table.addEventListener('mouseout', function (event) {
            const hoverEndTime = new Date().getTime();
            const hoverDuration = (hoverEndTime - hoverStartTime) / 1000; // Convert to seconds

            // Extract relevant information for recording
            const component = 'entire_vitals_table';

            // Send AJAX request to the server
            sendHoverEvent(component, hoverDuration);
        });*/

        // Attach event listeners to each row for hover events
        const rows = Array.from(table.getElementsByTagName('tr'));
        console.log('rows:', rows)
        rows.forEach(row => {
            // console.log('row:', row)
            row.addEventListener('mouseover', function (event) {
                hoverStartTime = new Date().getTime();
            });
            console.log('Hover - table');

            row.addEventListener('mouseout', function (event) {
                const hoverEndTime = new Date().getTime();
                const hoverDuration = (hoverEndTime - hoverStartTime) / 1000; // Convert to seconds

                // Extract relevant information for recording
                const component = `vitals_table_${row.cells[0].textContent}`; // Updated metric with prefix

                // Send AJAX request to the server
                sendHoverEvent(component, hoverDuration);
            });
        });

        // Attach event listeners to the echarts plot for hover events
        plot.addEventListener('mouseover', function (event) {
            hoverStartTime = new Date().getTime();
        });
        console.log('Hover - plot');
        plot.addEventListener('mouseout', function (event) {
            const hoverEndTime = new Date().getTime();
            const hoverDuration = (hoverEndTime - hoverStartTime) / 1000; // Convert to seconds

            // Extract relevant information for recording
            const component = 'echarts_plot';

            // Send AJAX request to the server
            sendHoverEvent(component, hoverDuration);
        });

        /*// Attach event listeners to the card for hover events
        card.addEventListener('mouseover', function (event) {
            hoverStartTime = new Date().getTime();
        });
        console.log('Hover - card');
        card.addEventListener('mouseout', function (event) {
            const hoverEndTime = new Date().getTime();
            const hoverDuration = (hoverEndTime - hoverStartTime) / 1000; // Convert to seconds

            // Extract relevant information for recording
            const component = 'patient_card';

            // Send AJAX request to the server
            sendHoverEvent(component, hoverDuration);
        });*/

        // Attach event listeners to each definition term (<dt>) for hover events
        const dtElements = card.querySelectorAll('dt');
        dtElements.forEach(dt => {
            dt.addEventListener('mouseover', function (event) {
                hoverStartTime = new Date().getTime();
            });
            console.log('Hover - dtElements');
            dt.addEventListener('mouseout', function (event) {
                const hoverEndTime = new Date().getTime();
                const hoverDuration = (hoverEndTime - hoverStartTime) / 1000; // Convert to seconds

                // Extract relevant information for recording
                const component = `patient_details_${dt.textContent.toLowerCase().replace(/\s+/g, '_')}`;

                // Send AJAX request to the server (assuming you have a sendHoverEvent function)
                sendHoverEvent(component, hoverDuration);
            });
        });

        // Attach event listeners to each definition description (<dd>) for hover events
        const ddElements = card.querySelectorAll('dd');
        ddElements.forEach(dd => {
            dd.addEventListener('mouseover', function (event) {
                hoverStartTime = new Date().getTime();
            });
            console.log('Hover - ddElements');
            dd.addEventListener('mouseout', function (event) {
                const hoverEndTime = new Date().getTime();
                const hoverDuration = (hoverEndTime - hoverStartTime) / 1000; // Convert to seconds

                // Extract relevant information for recording
                const component = `patient_details_${dd.previousElementSibling.textContent.toLowerCase().replace(/\s+/g, '_')}`;

                // Send AJAX request to the server (assuming you have a sendHoverEvent function)
                sendHoverEvent(component, hoverDuration);
            });
        });

        // Attach event listeners to the guidelinesEmbed for hover events
        guidelinesEmbed.addEventListener('mouseover', function (event) {
            hoverStartTime = new Date().getTime();
        });
        console.log('Hover - guidelinesEmbed');
        guidelinesEmbed.addEventListener('mouseout', function (event) {
            const hoverEndTime = new Date().getTime();
            const hoverDuration = (hoverEndTime - hoverStartTime) / 1000; // Convert to seconds

            // Extract relevant information for recording
            const component = 'guidelines_pdf_simple';

            // Send AJAX request to the server
            sendHoverEvent(component, hoverDuration);
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