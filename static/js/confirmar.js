// Pede confirmação antes de enviar qualquer formulário marcado com data-confirmar
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("form[data-confirmar]").forEach(function (form) {
    form.addEventListener("submit", function (evento) {
      if (!confirm(form.dataset.confirmar)) {
        evento.preventDefault();
      }
    });
  });
});
