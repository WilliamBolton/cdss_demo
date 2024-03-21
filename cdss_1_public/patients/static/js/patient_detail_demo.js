document.addEventListener('DOMContentLoaded', function () {
    // Access the variables defined in the HTML file
    // vitalsDataJson and vitalsDataNoNanJson are now available here
    
    // Display CSV data in the table
    displayCsvData(vitalsDataNoNanJson);

    // Function to display JSON data in the table
    function displayCsvData(jsonData) {
                const table = document.getElementById("vitals-table");

                // Extract metrics and time data
                const metrics = jsonData.map(item => item["Metric / Time (hours)"]);
                const timePoints = Object.keys(jsonData[0]).filter(key => key !== "Metric / Time (hours)");

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
            }

    // Extract metrics and time data
    const metrics = vitalsDataJson.map(item => item["Metric / Time (hours)"]);
    const timePoints = Object.keys(vitalsDataJson[0]).filter(key => key !== "Metric / Time (hours)");

    // Set echarts options
    options = {
        title: {
            text: ''
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: metrics,
            selected: {}, // Empty initially, indicating all series are visible
        },
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
            // name: 'Hours',
        },
        yAxis: {
            type: 'value',
            // name: 'Value',
        },
        series: metrics.map(metric => ({
            name: metric,
            type: 'line',
            data: timePoints.map(timePoint => vitalsDataJson.find(item => item["Metric / Time (hours)"] === metric)[timePoint]),
            connectNulls:true
        })),
        dataZoom: [
        {
            type: 'inside',
            start: 0,
            end: 100,
        },
        {
            show: true,
            type: 'slider',
            bottom: 10,
            start: 0,
            end: 100,
            yAxisIndex: [0], // Specify the yAxisIndex for y-axis zoom
        },
        {
            show: true,
            type: 'slider',
            start: 0,
            end: 100,
            xAxisIndex: [0], // Specify the xAxisIndex for x-axis zoom
            height: '2%',
            bottom: 5
        },
    ],
    };

    // Initialize ECharts
    // Use the echartsData to create the line plot
    const echartsContainer = document.getElementById('echarts-container');
    const echartsInstance = echarts.init(echartsContainer);

    // Set the initial options
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