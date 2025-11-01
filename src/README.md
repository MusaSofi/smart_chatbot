# Chatbot for students

- [Installation](#installation)
    - [Local machine](#local-machine)
    - [Server machine (Remote)](#server-machine-remote)
    - [CPU instead of GPU](#cpu-instead-of-gpu)
- [Usage](#usage)

## Installation

### Local machine
1. Start all containers:
    >```docker compose -f docker-compose.yaml up -d``` 
2. Pull Ollama models:
    >```docker exec -it ollama ollama pull gemma3:12b```
    
    >```docker exec -it ollama ollama pull bge-m3```
3. Populate database and wait until you see "✅ Populating database is done": 
    >```docker exec -it flask_server python rag/populate_database.py```

### Server machine (Remote)
1. Go to the remote machine using tunneling, e.g.:
     >``` ssh -L 5000:localhost:5000 -L 5173:localhost:5173 shutova@ucs9.cs.univie.ac.at``` 

    important to tunnel two ports: 5000 and 5173.
2. Go to the folder with **docker-compose.yaml** file.
3. Start all containers:
    >```docker compose -f docker-compose.yaml up -d``` 
4. Pull Ollama models:
    >```docker exec -it ollama ollama pull gemma3:12b```
    
    >```docker exec -it ollama ollama pull bge-m3```
5. Populate database and wait until you see "✅ Populating database is done": 
    >```docker exec -it flask_server python rag/populate_database.py```

### CPU instead of GPU
Use the following command by docker composing:
>```docker compose -f docker-compose_cpu.yaml up -d```



## Usage

1. Start all containers, if they are not started yet:
    
    For GPU:
    >```docker compose -f docker-compose.yaml up -d```

    For CPU:
    >```docker compose -f docker-compose_cpu.yaml up -d```
2. Open in the Browser ***http://localhost:5173***
3. Enjoy the chat.