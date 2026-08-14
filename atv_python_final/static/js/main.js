(function () {
  const body = document.body;
  const botao = document.getElementById("btn-modo-escuro");

  function aplicarModo(ativo) {
    body.classList.toggle("modo-escuro", ativo);
    localStorage.setItem("modoEscuro", ativo ? "true" : "false");
  }

  aplicarModo(localStorage.getItem("modoEscuro") === "true");

  if (botao) {
    botao.addEventListener("click", function () {
      aplicarModo(!body.classList.contains("modo-escuro"));
    });
  }
})();
