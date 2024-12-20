echo Início do script: %date% %time% > log.txt

cd /d "C:\Users\Pedro\OneDrive\DataDom\1. Repositórios GitHub\Data-Science-Projects\1-ProphetCurrencyTrend" || echo "Erro ao mudar de diretório" >> log.txt

echo Diretório alterado: %date% %time% >> log.txt

echo Ultima atualização: %date% %time% > last_update.txt || echo "Erro ao atualizar last_update.txt" >> log.txt

git add . || echo "Erro no git add" >> log.txt

git commit -m "Commit automático diário em %date% %time%" || echo "Erro no git commit" >> log.txt

git push origin main || echo "Erro no git push" >> log.txt

echo "Commit e Push realizados com sucesso!" >> log.txt
echo Fim do script: %date% %time% >> log.txt
exit