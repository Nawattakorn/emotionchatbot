from flask import Flask, render_template, request, jsonify
import numpy as np
import pickle
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import random
app = Flask(__name__)

# Load emotion analysis model
emotion_model = tf.keras.models.load_model('models/sentiment_analysis_model.h5')
with open('models/tokenizer.pkl', 'rb') as f:
    emotion_tokenizer = pickle.load(f)
with open('models/encoder.pkl', 'rb') as f:
    encoder = pickle.load(f)
max_len = 50

# Rule-based responses
RESPONSE_RULES = {
    "anger": [
        "I can see this is really upsetting. Let's take a moment to breathe.",
        "That sounds incredibly frustrating. What's one small step we can take to address this?",
        "Anger is a natural emotion. Would you like to explore healthy ways to express it?",
        "I hear your frustration. Let's focus on solutions rather than problems."
    ],
    "fear": [
        "It's okay to feel scared. What's the smallest thing that could make you feel safer right now?",
        "Fear often comes from the unknown. Let's break this down into manageable parts.",
        "You're stronger than you think. What's helped you through tough times before?",
        "Let's imagine the best-case scenario instead of the worst. What might that look like?"
    ],
    "joy": [
        "Your happiness is contagious! What makes this moment special for you?",
        "Celebrate this win! How will you remember this positive experience?",
        "Joyful moments are precious. Let's brainstorm ways to extend this feeling!",
        "It's wonderful to hear you're feeling good! What are you grateful for right now?"
    ],
    "sadness": [
        "I'm here to sit with you in this sadness. You don't have to face it alone.",
        "Sadness can feel heavy. Would you like to share what's weighing on your heart?",
        "This pain won't last forever. What small comfort can you give yourself today?",
        "Your feelings are valid. Let's explore ways to nurture yourself through this."
    ],
    "default": [
        "Thank you for sharing. What would help you most right now?",
        "Let's explore this further. Could you tell me more?",
        "Your perspective matters. How can I best support you?",
        "Let's work through this together. What's your main priority at this moment?"
    ]
}
def predict_emotion(text):
    sequence = emotion_tokenizer.texts_to_sequences([text])
    padded_seq = pad_sequences(sequence, maxlen=max_len)
    probs = emotion_model.predict(padded_seq)[0]
    labels = encoder.classes_.tolist()
    return {label: float(prob) for label, prob in zip(labels, probs)}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data['text']
    
    # Predict emotion
    probabilities = predict_emotion(text)
    dominant_emotion = max(probabilities, key=probabilities.get)
    
    # Get random response
    responses = RESPONSE_RULES.get(dominant_emotion, RESPONSE_RULES['default'])
    
    response = generate_dynamic_response(dominant_emotion, probabilities)
    
    return jsonify({
        'emotion': dominant_emotion,
        'probabilities': probabilities,
        'response': response
    })
def generate_dynamic_response(emotion, probabilities):
    emotion_intensity = probabilities[emotion]
    
    templates = {
        "anger": [
            f"I sense {emotion_intensity*100:.0f}% frustration here. Let's channel that energy productively.",
            "This level of anger ({emotion_intensity*100:.0f}%) suggests something important to you. What's the core value being threatened?"
        ],
        "fear": [
            f"With {emotion_intensity*100:.0f}% anxiety, safety is key. Let's create a safety plan.",
            "This fear level ({emotion_intensity*100:.0f}%) needs careful handling. What's your safest next step?"
        ],
        "joy": [
            f"Wow, {emotion_intensity*100:.0f}% positivity! Let's amplify this feeling!",
            "Your {emotion_intensity*100:.0f}% joy is inspiring! How can we build on this momentum?"
        ],
        "sadness": [
            f"At {emotion_intensity*100:.0f}% sadness, self-care is crucial. Let's prioritize your needs.",
            "This depth of sadness ({emotion_intensity*100:.0f}%) deserves gentle care. What comforts you most?"
        ]
    }
    
    if random.random() < 0.3:  # 30% chance to use dynamic template
        return random.choice(templates.get(emotion, [""]))
    return random.choice(RESPONSE_RULES.get(emotion, RESPONSE_RULES['default']))

if __name__ == '__main__':
    app.run()