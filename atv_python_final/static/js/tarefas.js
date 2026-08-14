(function () {
  const selectStatus = document.getElementById("filtro-status");
  const lista = document.getElementById("lista-tarefas");

  const rotulos = {
    pendente: "Pendente",
    em_andamento: "Em andamento",
    concluida: "Concluída",
  };

  function escapeHtml(texto) {
    const div = document.createElement("div");
    div.textContent = texto ?? "";
    return div.innerHTML;
  }

  function renderizarTarefas(tarefas) {
    if (!tarefas.length) {
      lista.innerHTML = '<p class="text-muted">Nenhuma tarefa encontrada.</p>';
      return;
    }

    lista.innerHTML = tarefas
      .map(
        (tarefa) => `
      <div class="col-md-6 col-lg-4">
        <div class="card h-100 shadow-sm card-status-${tarefa.status}">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start">
              <h5 class="card-title">${escapeHtml(tarefa.titulo)}</h5>
              <span class="badge status-badge-${tarefa.status}">${rotulos[tarefa.status]}</span>
            </div>
            <p class="card-text">${escapeHtml(tarefa.descricao) || "Sem descrição."}</p>
          </div>
          <div class="card-footer bg-transparent d-flex justify-content-end gap-2">
            <a href="/editar/${tarefa.id}" class="btn btn-sm btn-outline-primary" title="Editar">
              <i class="bi bi-pencil-square"></i>
            </a>
            <form method="POST" action="/excluir/${tarefa.id}" onsubmit="return confirm('Excluir esta tarefa?');">
              <button type="submit" class="btn btn-sm btn-outline-danger" title="Excluir">
                <i class="bi bi-trash"></i>
              </button>
            </form>
          </div>
        </div>
      </div>`
      )
      .join("");
  }

  async function filtrarTarefas(status) {
    const url = status ? `/api/tarefas?status=${encodeURIComponent(status)}` : "/api/tarefas";
    try {
      const resposta = await fetch(url);
      if (!resposta.ok) throw new Error("Falha ao buscar tarefas");
      const tarefas = await resposta.json();
      renderizarTarefas(tarefas);
    } catch (erro) {
      console.error(erro);
    }
  }

  if (selectStatus) {
    selectStatus.addEventListener("change", function () {
      filtrarTarefas(this.value);
    });
  }
})();
