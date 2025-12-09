# AVANCE DE PROYECTO FINAL

## GRUPO 1

**Clínica veterinaria**: Mascota, Duenyo, Veterinario, Cita, Tratamiento

**Repo**: https://github.com/albanomp/Proyecto-Clinica-Veterinaria

- **Jorge**
- Albano
- Marcos

### PASOS
- Decidir entidades y relaciones: 100%
- Configuración BBDD: 100%
- Modelos SQLAlchemy: 100%
- Schemas Pydantic: 100%
- API REST CRUD: 80%
- Controladores web: 80%
- Pantallas HTML: 80%

---

## GRUPO 2

**Gestor de videojuegos**: Videogame, Genre, Developer, User

**Repo**: https://github.com/Mapakitus/gestor-videojuegos

- **Paco**
- Jon

### PASOS
- Decidir entidades y relaciones: 100%
- Configuración BBDD: 100%
- Modelos SQLAlchemy: 100%
- Schemas Pydantic: 100%
- API REST CRUD: 100%
- Controladores web: 70%
- Pantallas HTML: 70%

---

## GRUPO 3

**Cartelera de cine**: Pelicula, Venta, Sala, Genero, Horario

**Repo**: https://github.com/HueteDevs/Proyecto_Adecco

- Javi
- Reyes
- Kary
- Manuel

### PASOS
- Decidir entidades y relaciones: 100%
- Configuración BBDD: 90%
- Modelos SQLAlchemy: 100%
- Schemas Pydantic: 80%
- API REST CRUD: 80%
- Controladores web: 60%
- Pantallas HTML: 50%

---

## GRUPO 4

**Biblioteca**: Libro, Genero, Usuario, Carrito

**Repo**: https://github.com/RaresID/biblioteca-commerce

- **Rafael**
- Deme
- Alejandro Gómez

### PASOS
- Decidir entidades y relaciones: 100%
- Configuración BBDD: 70%
- Modelos SQLAlchemy: 75%
- Schemas Pydantic: 25%
- API REST CRUD: 0%
- Controladores web: 0% (priorizar)
- Pantallas HTML: 0% (priorizar)

---
---
---

## ESTRUCTURA BÁSICA DE PROYECTO
```
REPOSITORIO
- .venv (entorno virtual)
- app
    - models (modelos SQLAlchemy)
        - __init__.py
        - artist.py
        - song.py
    - routers (controladores)
        - api (API REST)
            - __init__.py
            - artists.py
            - songs.py
        - web (controladores web)
            - __init__.py
            - artists.py
            - home.py
            - songs.py
    - schemas (schemas Pydantic)
        - __init__.py
        - artist.py
        - song.py
    - static (archivos estáticos)
        - css (hojas de estilo)
            - styles.css
        - img (imágenes)
            - imagen1.jpg
            - imagen2.jpg
        - js (scripts javascript)
            - script.js
    - templates (plantillas Jinja2)
        - artists
            - detail.html
            - form.html
            - list.html
        - songs
            - detail.html
            - form.html
            - list.html
        - home.html
    - __init__.py
    - database.py (configuración base de datos)
    - main.py

- database.db (base de datos)
- .gitignore (archivos a ignorar)
- main.py
- README.md
- requirements.txt
```