// static/js/script.js

$(document).ready(function () {
  // Smooth scrolling effect for anchor links
  $("nav a").on("click", function (e) {
    e.preventDefault();
    var target = $(this).attr("href");
    $("html, body").animate(
      {
        scrollTop: $(target).offset().top - 50,
      },
      1000
    );
  });

  // Scroll to top button functionality
  $(window).scroll(function () {
    if ($(this).scrollTop() > 100) {
      $("#scrollTopBtn").fadeIn();
    } else {
      $("#scrollTopBtn").fadeOut();
    }
  });

  $("#scrollTopBtn").click(function () {
    $("html, body").animate({ scrollTop: 0 }, 1000);
  });
});
