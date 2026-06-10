from flask import Flask

app = Flask(__name__)

@app.route("/curriculo")
def decorate():
    return """
    <!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Envio de Currículo</title>
    <style>
        * { box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; margin: 0; padding: 40px 20px; color: #333; }
        .form-container { max-width: 600px; background: #ffffff; margin: 0 auto; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
        h2 { margin-top: 0; color: #1a73e8; border-bottom: 2px solid #e8f0fe; padding-bottom: 12px; font-size: 24px; }
        p { color: #666; font-size: 14px; margin-bottom: 25px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; font-weight: 600; margin-bottom: 8px; font-size: 14px; }
        .required::after { content: " *"; color: #d93025; }
        input[type="text"], input[type="email"], input[type="tel"], input[type="url"], select, textarea { width: 100%; padding: 12px; border: 1px solid #dadce0; border-radius: 6px; font-size: 15px; background-color: #fafafa; transition: border-color 0.2s; }
        input:focus, select:focus, textarea:focus { outline: none; border-color: #1a73e8; background-color: #fff; }
        textarea { height: 110px; resize: vertical; }
        input[type="file"] { padding: 8px 0; font-size: 14px; }
        button { background-color: #1a73e8; color: white; padding: 14px 20px; border: none; border-radius: 6px; cursor: pointer; width: 100%; font-size: 16px; font-weight: 600; transition: background-color 0.2s; }
        button:hover { background-color: #1557b0; }
    </style>
</head>
<body>

<div class="form-container">
    <h2>Banco de Talentos</h2>
    <p>Preencha os campos abaixo para cadastrar seu perfil em nossa base de dados profissionais.</p>

    <!-- O atributo enctype é mandatório para permitir o upload de documentos -->
    <form action="#" method="POST" enctype="multipart/form-data">
        
        <!-- Seção: Dados Pessoais -->
        <div class="form-group">
            <label for="nome" class="required">Nome Completo</label>
            <input type="text" id="nome" name="nome" placeholder="Ex: João Silva" required autocomplete="name">
        </div>

        <div class="form-group">
            <label for="email" class="required">E-mail</label>
            <input type="email" id="email" name="email" placeholder="nome@exemplo.com" required autocomplete="email">
        </div>

        <div class="form-group">
            <label for="telefone" class="required">Telefone / WhatsApp</label>
            <!-- O atributo pattern exige formato com DDD e 9 dígitos -->
            <input type="tel" id="telefone" name="telefone" placeholder="(11) 99999-9999" pattern="\([0-9]{2}\) [0-9]{5}-[0-9]{4}" required>
        </div>

        <div class="form-group">
            <label for="linkedin">Link do LinkedIn</label>
            <input type="url" id="linkedin" name="linkedin" placeholder="linkedin.com">
        </div>

        <!-- Seção: Perfil Profissional -->
        <div class="form-group">
            <label for="area">Área de Interesse</label>
            <select id="area" name="area">
                <option value="tecnologia">Tecnologia / Desenvolvimento</option>
                <option value="comercial">Comercial / Vendas</option>
                <option value="financeiro">Financeiro / Contabilidade</option>
                <option value="marketing">Marketing / Comunicação</option>
                <option value="rh">Recursos Humanos</option>
            </select>
        </div>

        <div class="form-group">
            <label for="experiencia">Nível de Experiência Atual</label>
            <select id="experiencia" name="experiencia">
                <option value="estagio">Estágio / Trainee</option>
                <option value="junior">Júnior</option>
                <option value="pleno">Pleno</option>
                <option value="senior">Sênior</option>
            </select>
        </div>

        <div class="form-group">
            <label for="resumo">Resumo de Qualificações</label>
            <textarea id="resumo" name="resumo" placeholder="Descreva brevemente suas principais experiências profissionais, ferramentas que domina ou conquistas recentes..."></textarea>
        </div>

        <!-- Seção: Upload -->
        <div class="form-group">
            <label for="curriculo" class="required">Anexe seu Currículo</label>
            <!-- O atributo accept restringe a janela de seleção a formatos específicos de texto -->
            <input type="file" id="curriculo" name="curriculo" accept=".pdf,.doc,.docx" required>
        </div>

        <button type="submit">Enviar Candidatura</button>
    </form>
</div>

</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug = True)