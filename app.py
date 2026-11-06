import os

from flask import Flask, render_template, redirect, url_for, request
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.exc import IntegrityError

from config import config
from logs import configura_logging
from models import db, Recado, Categoria
from forms import RecadoForm

# ---------------------------------------------------------------- criação da aplicação
app = Flask(__name__)
app.config.from_object(config[os.environ.get("APP_ENV", "development")])

if not app.config["SECRET_KEY"]:
    raise RuntimeError("Defina a variável de ambiente SECRET_KEY.")

configura_logging(app)
CSRFProtect(app)
db.init_app(app)


def opcoes_categorias():
    return [(c.id, c.nome) for c in Categoria.query.order_by(Categoria.nome).all()]


# ---------------------------------------------------------------- READ
@app.route("/")
def index():
    recados = Recado.query.order_by(Recado.id).all()
    return render_template("index.html", recados=recados, titulo="Meus Recados")


@app.route("/pendentes")
def pendentes():
    return render_template("index.html", recados=Recado.pendentes(), titulo="Recados Pendentes")


@app.route("/busca")
def busca():
    q = request.args.get("q", "")
    recados = Recado.query.filter(Recado.texto.contains(q)).order_by(Recado.id).all()
    app.logger.debug("Busca por %r retornou %d recado(s)", q, len(recados))
    return render_template("index.html", recados=recados, titulo=f"Busca por \"{q}\"")


@app.route("/categorias")
def categorias():
    todas = Categoria.query.order_by(Categoria.nome).all()
    return render_template("categorias.html", categorias=todas)


@app.route("/recado/<int:id>")
def detalhes(id):
    recado = db.get_or_404(Recado, id)
    return render_template("recado.html", recado=recado)


# ---------------------------------------------------------------- CREATE
@app.route("/novo", methods=["GET", "POST"])
def novo_recado():
    form = RecadoForm()
    form.categoria_id.choices = opcoes_categorias()
    if form.validate_on_submit():
        recado = Recado(texto=form.texto.data, descr=form.descr.data,
                        categoria_id=form.categoria_id.data)
        try:
            db.session.add(recado)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            app.logger.exception("Falha ao gravar recado %r", form.texto.data)
            raise
        app.logger.info("Recado criado: id=%s texto=%r", recado.id, recado.texto)
        return redirect(url_for("index"))
    return render_template("form.html", form=form, titulo="Novo recado")


# ---------------------------------------------------------------- UPDATE
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_recado(id):
    recado = db.get_or_404(Recado, id)
    form = RecadoForm(obj=recado)
    form.categoria_id.choices = opcoes_categorias()
    if form.validate_on_submit():
        recado.texto = form.texto.data
        recado.descr = form.descr.data
        recado.categoria_id = form.categoria_id.data
        db.session.commit()
        app.logger.info("Recado atualizado: id=%s", recado.id)
        return redirect(url_for("detalhes", id=recado.id))
    return render_template("form.html", form=form, titulo="Editar recado")


@app.route("/concluir/<int:id>", methods=["POST"])
def concluir_recado(id):
    recado = db.get_or_404(Recado, id)
    recado.concluido = True
    db.session.commit()
    app.logger.info("Recado concluído: id=%s", recado.id)
    return redirect(url_for("index"))


# ---------------------------------------------------------------- DELETE
@app.route("/deletar/<int:id>", methods=["POST"])
def deletar_recado(id):
    recado = db.get_or_404(Recado, id)
    db.session.delete(recado)
    db.session.commit()
    app.logger.warning("Recado removido: id=%s", id)
    return redirect(url_for("index"))


# ---------------------------------------------------------------- erros
@app.errorhandler(404)
def nao_encontrado(erro):
    app.logger.warning("404: %s %s", request.method, request.path)
    return render_template("404.html"), 404


@app.errorhandler(500)
def erro_interno(erro):
    return "<h1>Erro interno do servidor</h1><p>O problema foi registrado no log.</p>", 500


# ---------------------------------------------------------------- tabelas e carga inicial
def popula_banco():
    if Categoria.query.count() == 0:
        estudo, trabalho, pessoal = Categoria(nome="Estudo"), Categoria(nome="Trabalho"), Categoria(nome="Pessoal")
        db.session.add_all([estudo, trabalho, pessoal])
        db.session.add_all([
            Recado(texto="Revisar o Capítulo 3 de Flask",
                   descr="Reler o Capítulo 3 do livro e fazer os exercícios.",
                   concluido=True, categoria=estudo),
            Recado(texto="Estudar slides da Aula 8",
                   descr="Revisar a arquitetura e o roteiro de implantação.", categoria=estudo),
            Recado(texto="Entregar o Projeto Integrador",
                   descr="Publicar no PythonAnywhere e apresentar ao grupo.", categoria=trabalho),
        ])
        db.session.commit()
        app.logger.info("Banco populado com os dados iniciais")


with app.app_context():
    db.create_all()
    popula_banco()


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
