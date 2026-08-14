(function () {
  const rotulos = ["Pendente", "Em andamento", "Concluída"];
  const cores = ["#ffc107", "#0d6efd", "#198754"];

  async function carregarProgresso() {
    const resposta = await fetch("/api/progresso");
    const dados = await resposta.json();
    const valores = [dados.pendente || 0, dados.em_andamento || 0, dados.concluida || 0];

    new Chart(document.getElementById("grafico-barras"), {
      type: "bar",
      data: {
        labels: rotulos,
        datasets: [{ label: "Tarefas", data: valores, backgroundColor: cores }],
      },
      options: {
        scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } },
        plugins: { legend: { display: false } },
      },
    });

    new Chart(document.getElementById("grafico-pizza"), {
      type: "pie",
      data: {
        labels: rotulos,
        datasets: [{ data: valores, backgroundColor: cores }],
      },
    });
  }

  carregarProgresso();
})();
