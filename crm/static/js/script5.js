$(document).ready(function () {
  // Add form validation for required fields
  $("#registerForm").on("submit", function (e) {
    let isValid = true;

    // Check each input field
    $("input").each(function () {
      if ($(this).val().trim() === "") {
        isValid = false;
        $(this).addClass("is-invalid");
      } else {
        $(this).removeClass("is-invalid");
      }
    });

    if (!isValid) {
      e.preventDefault();
      alert("Please fill in all required fields.");
    }
  });

  // Add focus and blur event for form inputs for better UX
  $(".form-control").on("focus", function () {
    $(this).removeClass("is-invalid");
  });
});
