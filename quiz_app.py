import streamlit as st
from quiz_generator import generate_quiz_question_with_options

st.title('MCQ Quiz')

def reset_quiz_state():
    st.session_state.quiz_data = {}
    st.session_state.generated = False
    st.session_state.score = 0

if 'quiz_data' not in st.session_state:
    reset_quiz_state()

api_key = 'api_key' 
 
topic = st.text_input("Enter a topic for your quiz:", key="new_topic")
num_questions = st.number_input("How many questions do you want?", min_value=1, max_value=10, value=10, key="num_questions")

if st.button('Generate Quiz'):
    reset_quiz_state()
    st.session_state.generated = True
    for i in range(1, num_questions + 1):
        question, options, correct_answer = generate_quiz_question_with_options(topic, api_key)
        st.session_state.quiz_data[f"question_{i}"] = {"question": question, "options": options, "correct_answer": correct_answer}

if st.session_state.generated:
    for i in range(1, num_questions + 1):
        data = st.session_state.quiz_data[f"question_{i}"]
        st.write(f"Question {i}: {data['question']}")
        chosen_option = st.radio("Select your answer:", data['options'], key=f"answer_{i}_{st.session_state.new_topic}_{st.session_state.num_questions}")

if st.session_state.generated and st.button('Submit Answers'):
    score = 0
    for i in range(1, num_questions + 1):
        user_answer = st.session_state[f"answer_{i}_{st.session_state.new_topic}_{st.session_state.num_questions}"]
        correct_answer = st.session_state.quiz_data[f"question_{i}"]["correct_answer"]
        if user_answer == correct_answer:
            score += 1
    st.write(f"Your final score is {score}/{num_questions}")
    reset_quiz_state() 

if st.button('Start New Quiz'):
    if 'quiz_data' in st.session_state:
        del st.session_state['quiz_data']
