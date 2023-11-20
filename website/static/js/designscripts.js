var $progress = $('.progress');
var $progressBar = $('.progress-bar');
var $alert = $('.alert');
var $loading = $(".loading");

// setTimeout(function() {
//   $progressBar.css('width', '10%');
//   setTimeout(function() {
//       $progressBar.css('width', '30%');
//       setTimeout(function() {
//           $progressBar.css('width', '100%');
//           setTimeout(function() {
//             $(".loading").fadeOut();
//               $alert.css('display', 'block');
//           }, 500);
//       }, 5000);
//   }, 3000);
// }, 1000);

function reveal() {
  var reveals = document.querySelectorAll(".reveal");
  for (var i = 0; i < reveals.length; i++) {
    var windowHeight = window.innerHeight;
    var elementTop = reveals[i].getBoundingClientRect().top;
    var elementVisible = 150;
    if (elementTop < windowHeight - elementVisible) {
      reveals[i].classList.add("active");
    } else {
      reveals[i].classList.remove("active");
    }
  }
}

window.addEventListener("scroll", reveal);

var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})