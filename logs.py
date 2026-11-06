"""Configuração do logging da aplicação."""
import logging
import os
from logging.handlers import RotatingFileHandler


def configura_logging(app):
    os.makedirs(app.config["LOG_DIR"], exist_ok=True)

    formato = logging.Formatter(
        "%(asctime)s %(levelname)-8s [%(name)s] %(message)s")

    # arquivo com rotação: no máximo 3 arquivos de ~100 KB
    arquivo = RotatingFileHandler(
        os.path.join(app.config["LOG_DIR"], "app.log"),
        maxBytes=100_000, backupCount=3, encoding="utf-8")
    arquivo.setFormatter(formato)

    app.logger.addHandler(arquivo)
    app.logger.setLevel(app.config["LOG_LEVEL"])
    app.logger.info("Aplicação iniciada (debug=%s)", app.debug)
