// JavaScript to handle button color and click event

    document.addEventListener('DOMContentLoaded', function () {
    var completeButton = document.getElementById('completeButton');

    // Check completion status on page load
    checkCompletionStatus();

    function checkCompletionStatus() {
        var allPatients = Array.from(document.querySelectorAll('.patient-item'));
    
        // Print information about all patients and their form_filled_in status
        allPatients.forEach(function (patient) {
            console.log(`Patient ID: ${patient.dataset.patientId}, Form Filled In: ${patient.dataset.formFilledIn}, Form Filled In Type: ${typeof patient.dataset.formFilledIn}`);
        });

        var allPatientsFilledIn = allPatients.every(function (patient) {
            return patient.dataset.formFilledIn === 'True';
        });
        
        console.log('All Patients Filled In:', allPatientsFilledIn);
        // console.log('All Patients Filled In type:',typeof allPatientsFilledIn);

        if (allPatientsFilledIn) {
            // If all patients are filled in, enable the 'Complete' button and set it to primary color
            completeButton.removeAttribute('disabled');
            completeButton.classList.remove('btn-secondary');
            completeButton.classList.add('btn-primary');
        } else {
            // If not all patients are filled in, disable the 'Complete' button and set it to secondary color
            completeButton.setAttribute('disabled', 'disabled');
            completeButton.classList.remove('btn-primary');
            completeButton.classList.add('btn-secondary');
        }
    }

    // Add click event to 'Complete' button
    completeButton.addEventListener('click', function () {
        // Redirect to logout URL or perform logout action
        window.location.href = '{% url 'logout' %}';
    });

    // Listen for changes in the form_filled_in attribute
    document.addEventListener('change', function (event) {
        if (event.target.classList.contains('patient-item')) {
            checkCompletionStatus();
        }
    });
});