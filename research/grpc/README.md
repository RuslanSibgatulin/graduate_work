# Сравнительный тест grpc, fastapi и falsk


## Компиляция .proto файла

    mkdir builds 
    python -m grpc_tools.protoc -I protobufs/ --python_out=builds/ --grpc_python_out=builds/ protobufs/service.proto


## Запуск серверов и тест

    python server.py
    python test_client_grps.py

    python flask_server.py
    python test_client_rest.py

    python fastapi_server.py
    python test_client_rest.py


## Результат

Тестовым клиентом было сделано N запросов к серверу. Время обработки в секундах для каждого из фреймворков приведено в таблице

Запросов| FastAPI    | Flask     | gRPC      |
--------|------------|-----------|-----------|
10000   |16.619772   |20.925504  |7.555936   |
2000    |4.050370    |4.542745   |1.777085   |
1       |0.004537    |0.005655   |0.001922   |
