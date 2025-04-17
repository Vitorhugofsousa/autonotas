@echo off
echo Desinstalador das Notas Autoadesivas - INSS
echo =======================================
echo.

set INSTALL_DIR=%PROGRAMFILES%\Notas INSS

echo Removendo atalhos...
del "%USERPROFILE%\Desktop\Notas Autoadesivas - INSS.lnk"

echo Removendo registro de inicialização automática...
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "NotasINSS" /f 2>nul

echo Removendo arquivos...
del "%INSTALL_DIR%\Notas INSS.exe"
del "%INSTALL_DIR%\icon.png"
rmdir "%INSTALL_DIR%"

echo.
echo Desinstalação concluída!
echo.
echo Pressione qualquer tecla para sair...
pause > nul