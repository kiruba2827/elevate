// Prevent back navigation
history.pushState(null, null, location.href);
window.onpopstate = function () {
  history.pushState(null, null, location.href);
};
