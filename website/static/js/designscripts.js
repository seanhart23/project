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

var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})