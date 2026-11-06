# Lista de Recados — Exemplo da Aula 08 (Organização e Implantação)

Mesma aplicação da Aula 07, agora **organizada** e **pronta para produção**: configuração separada do código, variáveis de ambiente, logging e arquivos estáticos próprios. Roteiro de implantação no **PythonAnywhere** em `deploy/`.

## Estrutura

```
aula08_exemplo/
├── app.py            criação da aplicação, rotas e tratadores de erro
├── config.py         classes de configuração (desenvolvimento / produção) e leitura do .env
├── logs.py           configuração do logging (arquivo com rotação)
├── models.py         db, Categoria e Recado
├── forms.py          RecadoForm (Flask-WTF)
├── static/
│   ├── css/estilo.css    CSS próprio
│   └── js/confirmar.js   JavaScript próprio (confirmação antes de remover)
├── templates/
│   ├── base.html, index.html, recado.html, form.html, categorias.html, 404.html
│   └── partials/_navbar.html   trecho reutilizado com {% include %}
├── deploy/pythonanywhere_wsgi.py   modelo do arquivo WSGI
├── .env.example      modelo das variáveis de ambiente (copie para .env)
├── .gitignore        ignora .env, instance/, logs/, venv/
└── requirements.txt
```

## Executar localmente

```bash
python -m venv venv
source venv/bin/activate            # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                # Windows: copy .env.example .env
python app.py                       # http://127.0.0.1:5000
```

## Variáveis de ambiente

| Variável | Uso | Padrão |
|---|---|---|
| `APP_ENV` | `development` ou `production` | `development` |
| `SECRET_KEY` | chave de sessão e CSRF (**obrigatória em produção**) | chave de desenvolvimento |
| `DATABASE_URL` | URI do banco | `sqlite:///recados.db` |
| `LOG_LEVEL` | nível do log | `DEBUG` (dev) / `INFO` |

Gerar uma chave: `python -c "import secrets; print(secrets.token_hex(32))"`

## Logging

Os registros vão para `logs/app.log` (rotação em 3 arquivos de ~100 KB) e também para o terminal.
Crie, edite, conclua e remova recados e acompanhe: `tail -f logs/app.log`.

## O que mudou em relação à Aula 07

| Aula 07 | Aula 08 |
|---|---|
| `SECRET_KEY` e URI do banco dentro do `app.py` | `config.py` + variáveis de ambiente (`.env`) |
| Sem registro de eventos | `app.logger` e arquivo `logs/app.log` |
| Navbar dentro do `base.html` | `templates/partials/_navbar.html` com `{% include %}` |
| Só Bootstrap | CSS e JS próprios em `static/` (`url_for('static', ...)`) |
| `debug=True` fixo | `DEBUG` depende do ambiente |

## Implantação no PythonAnywhere (resumo)

1. Enviar o projeto (`git clone` em um console Bash).
2. `mkvirtualenv --python=python3.XX venv` e `pip install -r requirements.txt`.
3. Aba **Web** > *Add a new web app* > *Manual configuration* (mesma versão do Python).
4. Informar o caminho do virtualenv e editar o **arquivo WSGI** (modelo em `deploy/pythonanywhere_wsgi.py`).
5. Criar o `.env` no servidor com `APP_ENV=production` e uma `SECRET_KEY` própria.
6. Em *Static files*: URL `/static/` → `/home/seuusuario/<pasta-do-projeto>/static`.
7. Clicar em **Reload** e conferir os logs (*Error log*, *Server log*) e o `logs/app.log`.

Para atualizar: `git pull` no console e **Reload**.

## Problemas comuns

- **`RuntimeError: Defina a variável de ambiente SECRET_KEY`**: falta o `.env` (ou a variável) no ambiente de produção.
- **Página sem estilo no servidor**: faltou mapear `/static/` na aba Web.
- **`ModuleNotFoundError`**: o virtualenv da aba Web não é o que recebeu o `pip install`.
- **Mudei o código e nada mudou**: faltou clicar em Reload.

## Exercícios

1. Criar `TestingConfig` com banco em memória (`sqlite://`) e selecioná-la com `APP_ENV=testing`.
2. Registrar no log um aviso quando alguém buscar por texto vazio.
3. Adicionar um favicon em `static/img/` e referenciá-lo no `base.html`.
4. Transformar as rotas de recados em um *Blueprint*.
