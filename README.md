# Architecture Diagram – Diagram-as-Code (Python)

Este repositorio muestra cómo crear **diagramas de arquitectura como código** usando [Diagrams (mingrammer)](https://diagrams.mingrammer.com/).  
El enfoque *diagram-as-code* permite **documentar arquitecturas técnicas** de manera reproducible, versionada y sin exponer información sensible.

## ✨ Características
- Ejemplo genérico de arquitectura multi-cloud.
- Uso de múltiples iconos (Azure, GCP, NGINX, CI/CD, observabilidad, etc.).
- Fácil de extender y adaptar a otros contextos.
- Diagrama generado automáticamente en formato PNG.

## 🏗️ Arquitectura de ejemplo
El diagrama incluido refleja un patrón de referencia genérico:

- **Usuarios → CDN → WAF/Firewall → Load Balancer → Web/API**
- **Cache Redis** para acelerar respuestas.
- **Event Bus (Kafka)** y **Workers** para procesamiento asíncrono.
- **Base de datos relacional (SQL)** como almacenamiento persistente.
- **CI/CD (GitLab + Jenkins)** para construcción y despliegue de artefactos.
- **Observabilidad** con Prometheus y Grafana.
- **Bastion** para administración segura.
- **Batch/Jobs** para procesamiento offline.

⚠️ Nota: esta es una **arquitectura de ejemplo**, no corresponde a ningún sistema real.

## 📦 Estructura
```
.
├── example_architecture.py   # Script Python que genera el diagrama
├── requirements.txt          # Dependencias de Python
├── README.md                 # Este documento
├── LICENSE                   # Licencia MIT
└── .gitignore                # Ignora salidas y entornos locales
```

## 🔧 Requisitos
- Python **3.10+**
- [Graphviz](https://graphviz.org/) instalado en el sistema
- Paquete `diagrams`

## 🚀 Instalación
```bash
# Crear y activar un entorno virtual
python -m venv .venv && source .venv/bin/activate   # (Linux/macOS)
# En Windows:
# .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## 🖼️ Generar el diagrama
```bash
python example_architecture.py
# Resultado: reference-architecture.png en el directorio raíz
```

## 🛡️ Buenas prácticas
- Usa nombres **genéricos** (Web, API, Worker).
- Evita exponer IPs, dominios, secretos o rutas internas.
- Versiona diagramas junto al código para facilitar revisiones y auditorías.

## 📜 Licencia
MIT (ver `LICENSE`).