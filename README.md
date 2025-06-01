# Установка ollama 
```curl -fsSL https://ollama.com/install.sh | sh```

# Установка llama3 4-,bnye.
```ollama pull llama3:8b-instruct-q4_0```

# Запуск llama3 как сервер для доступо по api, запускает сервер на localhost:11434
```ollama serve```

# Установка зависимости для создания запроса к api llama3
```pip install requests```