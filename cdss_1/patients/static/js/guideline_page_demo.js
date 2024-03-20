document.addEventListener('DOMContentLoaded', function () {

    // Click tracker

    // Function to send AJAX request
    function trackLinkClick(linkId) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/track_link_click/');

        // Include CSRF token in headers
        var csrfToken = getCSRFToken();

        console.log('csrfToken:', csrfToken);

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

                console.log('We are here!');
                xhr.send(JSON.stringify({ linkId: linkId, patientId: patientName }));
            }
        }
    }

    // Add event listener for 'guidelines' link
    var guidelinesLink = document.getElementById('guidelinesLink');
    // console.log('guidelinedetailsLink');
    guidelinesLink.addEventListener('click', function () {
        trackLinkClick('guidelinesLink');
    });

    // Track hovering

    // Variables to track hover start time
    const flowchart = document.querySelector('.container');
    const embedElement = document.querySelector('embed[src*="Final_IV_to_Oral_Switch_Decision_Aid_based_on_NationalCriteria_UKHSA.pdf"]');

    let hoverStartTime;

    // Attach event listeners to the flowchart for hover events
    flowchart.addEventListener('mouseover', function (event) {
        hoverStartTime = new Date().getTime();
    });
    console.log('Hover - flowchart');
    flowchart.addEventListener('mouseout', function (event) {
        const hoverEndTime = new Date().getTime();
        const hoverDuration = (hoverEndTime - hoverStartTime) / 1000; // Convert to seconds

        // Extract relevant information for recording
        const component = 'guidelines_flowchart';

        // Send AJAX request to the server
        sendHoverEvent(component, hoverDuration);
    });

    // Attach event listeners to the embedElement for hover events
    embedElement.addEventListener('mouseover', function (event) {
        hoverStartTime = new Date().getTime();
    });
    console.log('Hover - embedElement');
    embedElement.addEventListener('mouseout', function (event) {
        const hoverEndTime = new Date().getTime();
        const hoverDuration = (hoverEndTime - hoverStartTime) / 1000; // Convert to seconds

        // Extract relevant information for recording
        const component = 'guidelines_pdf';

        // Send AJAX request to the server
        sendHoverEvent(component, hoverDuration);
    });
    
    // sendHoverEvent function
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