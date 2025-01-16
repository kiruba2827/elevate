$(document).ready(function () {
  // Example of form validation with jQuery
  $("form").submit(function (event) {
    var isValid = true;
    $("input[type='text'], input[type='password'], input[type='email']").each(
      function () {
        if ($(this).val() === "") {
          isValid = false;
          $(this).css("border-color", "red");
        } else {
          $(this).css("border-color", "#ddd");
        }
      }
    );

    if (!isValid) {
      event.preventDefault();
      alert("Please fill out all fields.");
    }
  });
});
