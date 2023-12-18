from langchain.llms import OpenAI

def generate_quiz_question_with_options(topic, api_key):
    llm = OpenAI(api_key='api_key')

    prompt = f"Create a multiple choice quiz question about {topic}, along with 4 options (A, B, C, D) and indicate the correct answer."
    response = llm(prompt, max_tokens=150, temperature=0.7).strip()
    
    return parse_response(response)

def parse_response(response):
    
    lines = response.split('\n')
    question = lines[0].split(": ", 1)[1]

    options = []
    for line in lines[1:5]:
        option_parts = line.split(') ', 2) if ') ' in line else line.split('. ', 2)
        if len(option_parts) > 1:
            options.append(option_parts[1].strip())
        else:
            options.append("Option not found")
    correct_answer_letter = lines[-1].split(": ")[1].strip()
    if correct_answer_letter:
        correct_answer_letter = correct_answer_letter[0]

    correct_option_index = ord(correct_answer_letter.upper()) - ord('A')  
    correct_option = options[correct_option_index] if 0 <= correct_option_index < len(options) else None

    return question, options, correct_option
