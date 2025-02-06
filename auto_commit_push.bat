echo Início do script: %date% %time% > log.txt

cd /d "C:\Users\Pedro\OneDrive\DataDom\1. Repositórios GitHub\Data-Science-Projects"

git add . || echo "Erro no git add" >> log.txt

git commit -m "Commit automático diário em %date% %time%" || echo "Erro no git commit" >> log.txt

git push origin main || echo "Erro no git push" >> log.txt

echo "Commit e Push realizados com sucesso!" >> log.txt
echo Fim do script: %date% %time% >> log.txt
exit