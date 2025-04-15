# Unit+e2e тесты

## Установка
```
pip install -r requirements.txt
```

## Настройка
```
export BASE_URL="http://localhost:8080/"
```
*Может понадобится*
```
export PATH="$PWD/.venv/bin:$PATH"
```

## Запуск
```
pytest tests/<тест>
```

*Для запуска всех тестов сразу*
```
pytest tests/*
```
