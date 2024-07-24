// JavaScript to make the navbar sticky after scrolling
window.onscroll = function() {makeNavbarSticky()};

var navbar = document.querySelector(".navbar");
var sticky = navbar.offsetTop;

function makeNavbarSticky() {
    if (window.pageYOffset >= sticky) {
        navbar.classList.add("sticky");
    } else {
        navbar.classList.remove("sticky");
    }
}