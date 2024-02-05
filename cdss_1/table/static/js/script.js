// Add a click event listener to highlight the clicked row
document.addEventListener('DOMContentLoaded', function () {
    var tableRows = document.querySelectorAll('tbody tr');

    tableRows.forEach(function (row) {
        row.addEventListener('click', function () {
            tableRows.forEach(function (r) {
                r.classList.remove('selected-row');
            });

            this.classList.add('selected-row');
        });
    });
});