console.log("JavaScript code is executing!");

document.addEventListener("DOMContentLoaded", function () {
    // Parse JSON data passed from Django view
    const vitalsDataJson = JSON.parse("{{ vitals_data_json|escapejs }}");

    // Display CSV data in the table
    displayCsvData(vitalsDataJson);

    // Function to display JSON data in the table
    function displayCsvData(jsonData) {
        const table = document.getElementById("vitals-table");

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
            Object.values(dataRow).forEach(value => {
                const td = document.createElement("td");
                td.textContent = value;
                row.appendChild(td);
            });
            table.appendChild(row);
        });
    }
});