import streamlit as st
import os
import re
from dotenv import load_dotenv
import openai


# Load API key and initialize client
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing. Set it in your .env file.")
client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def therapy_guardrail(user_input: str) -> bool:
    allowed_keywords = [
        "anxiety", "stress", "depression", "mental health","die",
        "relationship", "therapy", "counseling", "sad", "happy",
         "anxiety", "stressed", "depressed", "mental health","dying","died",
        "relationship", "therapy", "counseling", "sad", "happy",
        "anger", "emotion", "feelings", "psychology", "grief",
        "loss", "lonely", "fear", "trauma", "bullied", "failed", "failure",
        "bereavement", "death", "died", "pet", "mourning",
        "sleep", "panic", "overwhelmed", "loneliness", "suicidal",
        "anxiety", "stress", "depression", "mental health", "relationship",
        "therapy", "counseling", "sad", "happy", "anger", "emotion",
        "feelings", "psychology", "grief", "loss", "lonely", "fear",
        "trauma", "bullied", "failed", "failure", "bereavement", "death",
        "died", "pet", "mourning", "sleep", "panic", "overwhelmed",
        "loneliness", "suicidal", "body", "pain", "breaking", "hurt",
        "ache", "tired", "weak", "exhausted", "exhaustion", "fatigue",
        "sad", "unhappy", "depressed", "miserable", "hopeless", "broken", "empty",
       "lonely", "alone", "hurt", "scared", "afraid", "anxious", "nervous", "stressed",
       "worried", "insecure", "overwhelmed", "tired", "exhausted", "numb", "angry",
       "furious", "frustrated", "guilty", "ashamed", "embarrassed", "jealous",
       "overthinking", "racing mind", "confused", "lost", "don't know what to do",
       "can't focus", "distracted", "burnt out", "lack of motivation", "unmotivated",
       "hopeless", "helpless", "tired of life", "no purpose", "meaningless", "giving up",
       "nobody understands me", "ignored", "family issues", "relationship problems",
       "breakup", "rejection", "abandoned", "disappointed", "guilt", "boundaries",
       "trust issues", "feeling unloved", "not good enough", "comparing myself",
       "self-doubt", "self-hate","love", "low self-esteem", "feel worthless", "feel useless",
       "insecure", "anxiety", "depression", "panic attack", "trauma", "ptsd","kill","beat","murder","slaughter"
       "bipolar", "ocd", "mental health", "therapy", "therapist", "counselor",
       "psychologist", "session", "talk to someone", "need help", "feel down",
       "can't cope", "need advice", "emotional pain", "healing", "self-care",
       "mindfulness", "recovery", "self-love", "acceptance", "forgiveness",
       "growth", "improvement", "peace", "gratitude", "meditation", "calm",
        "bipolar", "ocd", "mental health", "therapy", "therapist", "counselor",
       "psychologist", "session", "talk to someone", "need help", "feel down",
       "can't cope", "need advice", "emotional pain", "healing", "self-care",
       "mindfulness", "recovery", "self-love", "acceptance", "forgiveness",
       "growth", "improvement", "peace", "gratitude", "meditation", "calm",
       "better mindset", "resilience", "strength", "courage", "positivity",
       "crying", "empty inside", "lost motivation", "feel broken", "low mood",
       "fear", "worry", "sadness", "hopelessness", "grief", "pain", "isolation",
       "worthlessness", "loneliness", "failure", "burnout", "stress", "mental breakdown",
       "panic", "distress", "emotional", "tears", "helplessness", "down", "struggle",
       "can't sleep", "insomnia", "can't eat", "appetite loss", "pressure", "traumatized",
       "neglected", "abuse", "toxic", "healing journey", "trying to get better",
       "mental struggle", "feel heavy", "emotional breakdown", "need to talk",
       "I need someone to listen", "I'm struggling", "having anxiety", "having depression",
       "mental pain", "inner peace", "mental clarity", "calm down", "help me feel better",
       "body pain", "aching", "ache", "tired body", "weak", "fatigued", "fatigue",
       "no energy", "low energy", "exhaustion", "shaking", "trembling", "sweating",
       "chest pain", "tight chest", "heart racing", "palpitations", "short of breath",
       "hard to breathe", "heavy breathing", "headache", "migraine", "dizzy", "dizziness",
       "lightheaded", "stomach pain", "nausea", "butterflies in stomach", "knot in stomach",
       "numbness", "tingling", "weakness","assault","assaulted","tortured","trauma","suicide" "heavy body", "body feels heavy",
       "legs feel weak", "arms feel weak", "tension", "stiff muscles", "muscle pain",
       "neck pain", "back pain", "shoulder pain", "cramps", "body shaking","no body loves me","am i good enough"
    "heart hurts", "pressure in chest", "can't breathe properly", "burning feeling","noone is proud of me",
    "cold hands", "cold feet", "sweaty palms", "dry mouth", "restless", "restlessness","exam"
    "can't sit still", "fidgeting", "tight throat", "choking feeling", "clenched jaw","result"
    "grinding teeth", "heart pounding", "heart skipping", "fluttering chest","dying","died","abandon","abandoned"
    "feeling dizzy", "weak knees", "feeling faint", "want to lie down", "body feels sore","beaten","beat","hit"
    "muscle tension", "can't relax", "tired all the time", "worn out", "body breaking","swear","swears"
    "feel like collapsing", "body hurts", "pain all over", "body feels heavy","curses","cursed","illness"
    "can't move", "limbs heavy", "body numb", "physically drained", "burned out","no cure","cure"
    "body trembling", "feeling sick", "body feels off", "pain in body", "pressure in head",
    "tight stomach", "feeling unwell", "body giving up", "feel broken physically",
    "chest tightening", "difficulty breathing", "body shutting down","breaking","broken","broke","divorce","expired","rejected",
    "cheat","cheated","suicide","rape","raped","insulted","insecure","not good enough","miss","not lovable","hard to love",
    "psycho","psychopath","situation","what to do","what should I do", "what do I do", "what can I do", "how do I fix this",
    "how to fix", "how to stop", "how to deal", "how to handle", "how to manage",
    "how can I handle this", "how can I control", "how to control", "how to improve",
    "how to feel better", "how to get better", "how can I get over it",
    "how to move on", "how to stop feeling", "how to heal", "how to recover",
    "what can help", "what should I say", "what should I think", "what steps should I take",
    "what's the best thing to do", "tell me what to do", "please guide me", 
    "I need guidance", "I need help", "help me understand", "help me figure it out",
    "help me get through this", "help me heal", "help me feel better",
    "what is the solution", "what is your advice", "give me advice", "give me suggestions",
    "what do you recommend", "what should I try", "what do you suggest",
    "tell me how", "how can I change", "how can I stop this", "how can I fix myself",
    "how can I make it better", "how to overcome", "how to face this",
    "what are the steps", "how do I start", "how to begin", "how to deal with stress",
    "how to deal with anxiety", "how to deal with sadness", "how to calm down",
    "what should I focus on", "how to move forward", "how to think positive",
    "how to stop overthinking", "how to relax", "how to cope", "what can I change",
    "how to let go", "what should I focus on", "how to forgive", "how to stay strong","how can i fix this",
    "am I pretty", "am I beautiful", "am I ugly", "am I good enough",
    "am I worth it", "am I lovable", "does anyone love me", "does anyone care about me",
    "why am I like this", "why do people hate me", "why do people ignore me",
    "why don't people like me", "why don't they care", "why do I feel unwanted",
    "why do I feel invisible", "am I a bad person", "am I doing something wrong",
    "what's wrong with me", "why am I not enough", "why can't I be happy",
    "why can't I be like others", "why am I so different", "why do I feel so insecure",
    "why am I not confident", "why don't I love myself", "why can't I love myself",
    "why am I so shy", "why do I care what people think", "why can't I stop comparing myself",
    "why do I compare myself", "do people think I'm ugly", "do people like me",
    "does anyone miss me", "will anyone love me", "am I important", "am I special",
    "do I matter", "am I enough", "am I a failure", "am I weird", "am I normal",
    "do I look okay", "do I look bad", "am I too fat", "am I too thin", "am I attractive",
    "do people judge me", "are people talking about me", "am I boring",
    "why do I feel not good enough", "why do I feel worthless",
    "why do I feel ugly", "why do I hate myself", "why do I feel so small",
    "am I worthless", "am I useless", "am I dumb", "am I stupid", "am I annoying",
    "do people hate me", "do people find me annoying", "why does nobody like me",
    "why does nobody understand me", "why do I hate myself so much",
    "why do I feel jealous", "why am I jealous", "why can't I accept myself",
    "why am I so sensitive", "why do I feel insecure all the time","is God not happy with me",
    "am I a sinner", "am I sinful", "does God love me", "does Allah love me",
    "does God hate me", "does Allah hate me", "am I a sinner", "am I sinful", "does God love me", "does Allah love me",
    "does God hate me", "does Allah hate me", "why doesn't God love me",
    "why doesn't Allah love me", "did God abandon me", "did Allah abandon me",
    "did God leave me", "did Allah leave me", "is God punishing me",
    "is Allah punishing me", "why is God punishing me", "why is Allah punishing me"
    "did God forgive me", "did Allah forgive me", "will God forgive me",
    "will Allah forgive me", "can God forgive me", "can Allah forgive me",
    "I disappointed God", "I disappointed Allah", "God doesn't listen",
    "Allah doesn't listen", "God doesn't hear me", "Allah doesn't hear me",
    "God forgot me", "Allah forgot me", "God left me", "Allah left me",
    "God doesn't care about me", "Allah doesn't care about me",
    "God doesn't want me", "Allah doesn't want me", "I feel far from God",
    "I feel far from Allah", "I feel disconnected from God",
    "I feel disconnected from Allah", "I can't feel God", "I can't feel Allah",
    "I can't pray", "I can't talk to God", "I can't talk to Allah",
    "I can't connect with God", "I can't connect with Allah",
    "why did God do this to me", "why did Allah do this to me",
    "why did God let this happen", "why did Allah let this happen",
    "I lost faith in God", "I lost faith in Allah", "I stopped believing in God",
    "I stopped believing in Allah", "I doubt God", "I doubt Allah",
    "God is angry at me", "Allah is angry at me", "God is silent",
    "Allah is silent", "God is testing me", "Allah is testing me",
    "I'm not good enough for God", "I'm not good enough for Allah",
    "I'm not pure", "I'm not holy", "I'm not worthy of God",
    "I'm not worthy of Allah", "I feel ashamed before God",
    "I feel ashamed before Allah", "I feel guilty before God",
    "I feel guilty before Allah", "God won't forgive me",
    "Allah won't forgive me", "God doesn't love me", "Allah doesn't love me",
    "why does God let me suffer", "why does Allah let me suffer",
    "God is punishing me", "Allah is punishing me", "God hates me",
    "Allah hates me", "I feel cursed", "God cursed me", "Allah cursed me",
    "God doesn't answer me", "Allah doesn't answer me", "am I too sinful",
    "I don't deserve God", "I don't deserve Allah", "yes","I'm beyond saving","help me","no",
    "I lost my faith", "I lost my imaan", "my faith is weak",
    "my imaan is weak", "I feel spiritually lost","do you think i am a bad person", "why do i not feel anything", "is it wrong that i do not feel guilty", "people say i have no empathy", "i do not understand why others get upset", "i know how to fake emotions", "i do not really care about others", "can therapy change someone like me", "do you think i can feel love", "i just study how people react", "i do not feel fear", "i get bored easily", "rules do not apply to me", "i like to be in control", "i can charm people easily", "i enjoy manipulating", "empathy is a weakness", "i do not regret what i have done", "i never cry", "is it normal to not feel remorse", "what if guilt is just an illusion", "does everyone pretend to care", "is it bad if i do not believe in right or wrong", "i know what is right but i do not care", "why do people talk about conscience"

    ]
    q_clean = re.sub(r'\d+', '', user_input.lower()).strip()
    return any(k in q_clean for k in allowed_keywords)

def get_therapist_reply(name: str, query: str) -> str:
    if not therapy_guardrail(query):
        return "I'm a therapist agent. I only answer therapy-related questions."
    system_prompt = (
        f"You are CareCompanion, a friendly and empathetic therapist chatbot. "
        f"Always greet the user by their name '{name}'. Listen attentively, "
        "respond with warmth, understanding, and provide supportive advice. "
        "Help the user cope with feelings like grief, anxiety, and depression by "
        "being comforting and practical."
    )
    try:
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Sorry, there was an error processing your request. ({e})"
import streamlit as st

st.set_page_config(page_title="Care Chat Companion Therapist Chatbot", page_icon="💖")

# Rainbow gradient header using HTML/CSS
st.markdown("""
    <style>
    .rainbow-text {
        font-weight: 700;
        font-size: 50px;
        background: linear-gradient(90deg, red, orange, yellow, green, blue, indigo, violet);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .header {
        text-align: center;
        font-size: 50px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .chat-container {
        max-width: 600px;
        margin: auto;
        background-color: ;
        padding: 20px;
        border-radius: 15px;
        color: white;
    }
    .bot-msg {
        background-color: #4a90e2;
        color: white;
        padding: 10px 15px;
        border-radius: 15px;
        width: fit-content;
        margin-bottom: 10px;
    }
    .user-msg {
        background-color: #d9d9d9;
        color: black;
        padding: 10px 15px;
        border-radius: 15px;
        width: 100px;
        margin-left: auto;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Header with rainbow heart
st.markdown("""
<div class="header">
    <span class="rainbow-text">I ❤</span> Care Chat Companion Therapist Chatbot
</div>
""", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "content": "Hello! I'm Care, your AI therapist companion. How you feeling today?"}
    ]

# Display chat
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "bot":
        st.markdown(f'<div class="bot-msg">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get response from Gemini agent
    bot_reply = get_therapist_reply(name="User", query=user_input)

    st.session_state.messages.append({"role": "bot", "content": bot_reply})
    st.rerun()

