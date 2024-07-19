# Changelog
Todas as mudanças notáveis serão documentadas neste arquivo.
O formato é baseado em [Keep a Changelog](http://keepachangelog.com/pt-BR/1.0.0/) e este projeto adere ao padrão [Semantic Versioning](http://semver.org/lang/pt-BR/spec/v2.0.0.html).

## [Não liberado]
### Adicionado
### Corrigido
### Modificado
### Obsoleto
### Removido

## [0.1.52](api_face_detect/tags/0.1.52) - 2020-12-31
### Modificado
    - Update dlib face detector for negative values for landmarks.

## [0.1.51](api_face_detect/tags/0.1.51) - 2020-09-02
### Modificado
    - Update Docker file.
    - Gunicorn configuration.
    
## [0.1.4](api_face_detect/tags/0.1.4) - 2020-09-01
### Modificado
    - Update Docker file.
    - Gunicorn configuration.
    
## [0.1.3](api_face_detect/tags/0.1.3) - 2020-07-23 
### Adicionado
    - Endpoint /image/full-face-detect.
### Modificado
    - Version de Pillow==7.2.0.

## [0.1.2](api_face_detect/tags/0.1.2) - 2020-01-20 
### Modificado
    - Version de Pillow==5.3.0.
    - Version de dlib==19.18.0.

## [0.1.1](api_face_detect/tags/0.1.1) - 2020-01-20 
### Adicionado
    - flask Api
    - endpoint: face-detect
    - Docs Swagger
### Modificado
    - Update Dockerfile
### Removido
    - FastApi

## [0.1.0](api_face_detect/tags/0.1.0) - 2019-12-19
    Versão inicial
### Adicionado
    - Servidor uwsgi para produção.
    - Servidor werkzeug para desenvolvimento.
    - Testes unitários da API de face-detect.
    - Logging para /var/log/sauron/face-detect* e /var/log/sauron/uwsgi*.
### Modificado
    - Update Docker file and enable empacotamento Docker no Jenkinsfile.