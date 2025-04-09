import streamlit as st
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
import os
import time

# Set page config
st.set_page_config(page_title="AI StoryVerse Learning App", layout="centered")

# Local quiz bank
QUIZ_BANK = {
    "Math": {
        "Addition": [
            {"q": "What is 2 + 3?", "a": ["4", "5", "6"], "c": "5"},
            {"q": "What is 10 + 15?", "a": ["25", "20", "30"], "c": "25"}
        ],
        "Multiplication": [
            {"q": "What is 3 x 4?", "a": ["12", "9", "7"], "c": "12"},
            {"q": "What is 6 x 2?", "a": ["10", "12", "14"], "c": "12"}
        ]
    },
    "Science": {
        "Plants": [
            {"q": "What do plants need to grow?", "a": ["Water", "Gold", "Plastic"], "c": "Water"},
            {"q": "Which part of plant makes food?", "a": ["Leaf", "Root", "Stem"], "c": "Leaf"}
        ]
    }
}

# Story generator

def generate_story(subject, topic, grade):
    return f"Once upon a time in Grade {grade}, a curious child explored the world of {subject}. In the topic '{topic}', they discovered something magical that changed how they saw the world forever."

# Generate image with text

def generate_image(text, filename):
    img = Image.new('RGB', (720, 480), color=(73, 109, 137))
    d = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    d.text((10, 200), text, fill=(255, 255, 0), font=font)
    img.save(filename)

# Generate audio

def generate_audio(text, filename):
    tts = gTTS(text=text)
    tts.save(filename)

# Create video

def create_video(image_path, audio_path, output_path):
    clip = ImageClip(image_path).set_duration(8)
    clip = clip.set_audio(AudioFileClip(audio_path))
    clip.write_videofile(output_path, fps=24)

# Add JavaScript for Enter key submission
st.markdown("""
    <script>
    const form = window.parent.document.querySelector("form");
    form.addEventListener("keypress", function(e) {
        if (e.key === "Enter") {
            e.preventDefault();
            document.querySelector("button[kind='primary']").click();
        }
    });
    </script>
    """, unsafe_allow_html=True)

# UI
st.title("📚 AI-Based StoryVerse Learning App")
st.markdown("### 🚀 Learn through AI-Generated Stories, Images, Videos & Quizzes")

subject = st.selectbox("Select Subject", list(QUIZ_BANK.keys()))
grade = st.selectbox("Select Grade", ["1", "2", "3", "4", "5"])
topic = st.selectbox("Select Topic", list(QUIZ_BANK[subject].keys()))

if st.button("Generate Story & Learn"):
    story = generate_story(subject, topic, grade)
    st.subheader("🌟 Story")
    st.write(story)

    # Generate image
    image_path = "story_image.png"
    generate_image(story[:60], image_path)
    st.image(image_path, caption="Story Illustration")

    # Generate audio
    audio_path = "story_audio.mp3"
    generate_audio(story, audio_path)
    st.audio(audio_path)

    # Generate video
    video_path = "output_video.mp4"
    create_video(image_path, audio_path, video_path)
    st.video(video_path)

    st.subheader("📝 Quiz Time")
    score = 0
    for idx, q in enumerate(QUIZ_BANK[subject][topic]):
        st.write(f"**Q{idx + 1}: {q['q']}**")
        user_ans = st.radio("", q['a'], key=idx)
        if user_ans == q['c']:
            score += 1
    st.success(f"✅ You scored {score} out of {len(QUIZ_BANK[subject][topic])}")

    # Cleanup
    time.sleep(1)
    os.remove(image_path)
    os.remove(audio_path)
    os.remove(video_path)

st.markdown("---")
st.markdown("Made with ❤️ as a unique prototype never implemented in India 🇮🇳")
