@echo off
REM Caminho para o repositório local
cd "C:\Users\Pedro\OneDrive\DataDom\1. Repositórios GitHub\Data-Science-Projects\1-ProphetCurrencyTrend"

REM Atualiza o arquivo dummy (last_update.txt) com data e hora
echo Ultima atualização: %date% %time% > last_update.txt

REM Atualiza o repositório local caso haja mudanças remotas (opcional)
git pull

REM Adiciona todos os arquivos alterados
git add .

REM Cria um commit com uma mensagem contendo a data/hora
git commit -m "Commit automático diário em %date% %time%"

REM Efetua o push para o branch principal
git push origin main

REM Mensagem final (opcional)
echo "Commit e Push realizados com sucesso!"