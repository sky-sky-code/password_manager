# ManagerPassword
***
## Запуск
1. остановить локальный postgres ```sudo systemctl stop postgresql``` 
<br> в контейнере запускается собственный postgres сервер, где создается нужная бд (pm)
2. запустить контейнер ``sudo docker-compose up``
3. перейте на http://127.0.0.1:8080/api/schema/swagger-ui/

***
## Тесты 

1. запуск тестов в корне проекта ``pytest``
