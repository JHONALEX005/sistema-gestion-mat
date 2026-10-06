# Publicar este repositorio en GitHub

Este proyecto ya es un repositorio Git local con varios commits. Para que la docente vea el historial y se ejecute el pipeline, falta publicarlo en la cuenta del equipo.

1. Inicie sesión en GitHub y cree un repositorio vacío llamado **`sistema-gestion-mat`**. Al crearlo, no agregue un README, .gitignore o licencia desde la web, porque estos archivos ya existen localmente.
2. Abra una terminal en la carpeta `sistema-gestion-mat`.
3. Ejecute estos comandos, reemplazando `USUARIO` por el usuario o la organización de GitHub donde creó el repositorio:

```sh
git remote add origin https://github.com/USUARIO/sistema-gestion-mat.git
git push -u origin main
```

4. Abra el repositorio en GitHub. En **Actions**, compruebe que el flujo «Verificacion de compilacion» terminó correctamente.
5. Abra **Commits** y compruebe que aparecen los commits de aplicación, documentación e integración continua.
6. Entregue `nombre_repositorio.txt` (junto a esta carpeta en el paquete de entrega). Un integrante del equipo realiza el envío.

Si Git solicita autenticación, complete el acceso con su cuenta; no incluya contraseñas ni tokens en el proyecto. Si `origin` ya existe, revise la URL con `git remote -v` antes de cambiarla.

