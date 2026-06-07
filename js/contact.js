/* Contact form — AJAX submit to Formspree, no redirect.
   Honeypot field guards against bots. Inline status messages. */
(function () {
  document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById("contact-form");
    if (!form) return;
    var status = document.getElementById("form-status");

    form.addEventListener("submit", function (e) {
      e.preventDefault();

      // Honeypot: if filled, silently pretend success.
      var hp = form.querySelector('input[name="_gotcha"]');
      if (hp && hp.value) {
        status.textContent = "Thanks! Your message was sent.";
        status.className = "form-status ok";
        form.reset();
        return;
      }

      status.textContent = "Sending\u2026";
      status.className = "form-status";

      var data = new FormData(form);
      fetch(form.action, {
        method: "POST",
        body: data,
        headers: { Accept: "application/json" }
      })
        .then(function (res) {
          if (res.ok) {
            status.textContent = "Thanks! Your message was sent.";
            status.className = "form-status ok";
            form.reset();
          } else {
            return res.json().then(function (d) {
              var msg =
                d && d.errors && d.errors.length
                  ? d.errors.map(function (x) { return x.message; }).join(", ")
                  : "Something went wrong. Please try again.";
              status.textContent = msg;
              status.className = "form-status error";
            });
          }
        })
        .catch(function () {
          status.textContent = "Network error. Please try again.";
          status.className = "form-status error";
        });
    });
  });
})();
