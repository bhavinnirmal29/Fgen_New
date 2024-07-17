$(document).ready(function() {
    // Handle click event for navbar links
    $('.nav-link').on('click', function() {
        // Remove active class from all navbar links
        $('.nav-link').removeClass('active');
        // Add active class to the clicked navbar link
        $(this).addClass('active');
    });
});