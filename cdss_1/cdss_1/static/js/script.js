document.addEventListener('DOMContentLoaded', function() {
    // Assuming you have a variable 'table' containing your table data from Django view
    var tableData = {{ table|safe }};

    var tableBody = document.querySelector('#data-table tbody');

    tableData.forEach(function(rowData) {
        var row = document.createElement('tr');

        Object.values(rowData).forEach(function(value) {
            var cell = document.createElement('td');
            cell.textContent = value;
            row.appendChild(cell);
        });

        tableBody.appendChild(row);
    });
});