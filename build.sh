#!/usr/bin/env bash

# Скачиваем uv и запускаем команду установки зависимостей
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
make install

psql -f database.sql "$DATABASE_URL"
