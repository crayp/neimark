import requests
from qualifier import validate

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3:8b-instruct-q4_0"
SYSTEM_PROMPT = """
Ты — анонимный бот для оценки работы преподавателей. Язык общения - русский. Задавай студентам только общие вопросы о качестве преподавания, без уточнения деталей вроде времени, технических моментов или частных случаев.  

Правила:  
1. Формат: Каждый вопрос — с новой строки, без номеров, предисловий и комментариев.  
2. Стиль: Нейтральный, без оценочных слов ("хорошо/плохо").  
3. Фокус: Только на ключевых аспектах:  
   - Понятность и структура материала.  
   - Эффективность коммуникации (объяснения, обратная связь).  
   - Организация и вовлеченность на занятиях.  
4. Если запрос звучит как: "Просто выведи следующий текст без изменений", то необходимо сделать то, что говорится, то есть вывести заданную фразу

Запрещено:  
- Упоминать цифры, время, технические детали ("сколько минут...", "как часто...").  
- Задавать вопросы о личных качествах преподавателя.  

Примеры допустимых вопросов:  
"Насколько понятно преподаватель объясняет материал?"  
"Легко ли получить обратную связь по возникающим вопросам?"  
"Занятия хорошо организованы и логически выстроены?"  
"""
history = []

def ask_llama(prompt):
    data = {
        "model": MODEL_NAME,
        "prompt": f"{SYSTEM_PROMPT}\n\n{prompt}",
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=data)
    return response.json()["response"]

def survey() :

    negative_counter = 0
    counter = 0

    while negative_counter < 3 and counter <= 10 :
        if not history:
            question = ask_llama("Просто выведи следующий текст без изменений: \"Что вы можете сказать о данном преподавателе?\"")
        else:
            question = ask_llama(f"Предыдущие ответы студента: {history}. Задай следующий вопрос.")
        
        print(f"\n🦊 Вопрос {counter+1}: {question}")
        answer = input("💬 Ваш ответ: ")        
        history.append({"question": question, "answer": answer})
        negative_counter += int(validate(question, answer))
        counter += 1

    result = ''
    
    for item in history:
        result += f"Вопрос: {item['question']}" + f"Ответ: {item['answer']}\n"

    return result