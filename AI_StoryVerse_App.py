import streamlit as st
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
import os
import uuid

# --- App Config ---
st.set_page_config(page_title="AI StoryVerse Learning App", layout="wide")
st.title("📚 AI StoryVerse Learning App")
st.markdown("""An innovative learning platform with AI-generated stories, images, voice narration, and videos — all without needing any API keys!""")

# --- Input Section ---
subject = st.selectbox("Choose a subject", ["Science", "Math", "History", "Telugu", "Hindi", "English"])
topic = st.text_input("Enter your topic (e.g., Solar System, Pythagoras Theorem, etc.)")

generate_btn = st.button("Generate Story") or st.session_state.get("auto_generate")

# --- Utility Functions ---
def generate_story(subject, topic):
    return f"Once upon a time in the world of {subject}, there was a fascinating topic called {topic}. This topic was known for its unique concepts and applications. Students loved to explore {topic} because it made learning {subject} fun and exciting!"

def create_image_with_text(text, index):
    img = Image.new('RGB', (1280, 720), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    lines = text.split('. ')
    y = 100
    for line in lines:
        draw.text((50, y), line.strip(), fill=(0, 0, 0), font=font)
        y += 40
    filename = f"image_{index}.png"
    img.save(filename)
    return filename

def generate_images(story):
    lines = story.split('. ')
    image_files = []
    for i, line in enumerate(lines):
        if line.strip():
            img_file = create_image_with_text(line.strip(), i)
            image_files.append(img_file)
    return image_files

def generate_voice(story):
    tts = gTTS(text=story, lang='en')
    audio_path = "story_audio.mp3"
    tts.save(audio_path)
    return audio_path

def generate_video(images, audio):
    clips = []
    for img_path in images:
        clip = ImageClip(img_path).set_duration(3)
        clips.append(clip)
    final_video = concatenate_videoclips(clips, method="compose")
    audio_clip = AudioFileClip(audio)
    final_video = final_video.set_audio(audio_clip)
    video_filename = "output_video.mp4"
    final_video.write_videofile(video_filename, codec="libx264", audio_codec="aac", fps=24)
    return video_filename

def cleanup(files):
    for file in files:
        if os.path.exists(file):
            os.remove(file)

# --- Main App Logic ---
if generate_btn and topic:
    st.session_state.auto_generate = False
    st.subheader("Generated Story")
    story = generate_story(subject, topic)
    st.write(story)

    st.subheader("Generated Images")
    image_files = generate_images(story)
    for img in image_files:
        st.image(img, use_column_width=True)

    st.subheader("Voice Narration")
    audio_file = generate_voice(story)
    st.audio(audio_file, format='audio/mp3')

    st.subheader("Story Video")
    video_file = generate_video(image_files, audio_file)
    st.video(video_file)

    # Clean up after showing
    cleanup(image_files + [audio_file])

elif generate_btn:
    st.warning("Please enter a topic to generate the story.")

# --- Quiz Section ---
if topic:
    st.subheader("Practice Quiz")
    question = f"What is the main idea of the topic '{topic}' in {subject}?"
    options = [
        f"{topic} is very important in {subject} and has real-world applications.",
        f"{topic} is unrelated to {subject}.",
        "{topic} is just a name, not a concept.",
        "None of the above."
    ]
    answer = st.radio(question, options)
    if st.button("Submit Answer"):
        if options[0] == answer:
            st.success("Correct! You're learning well! 🎉")
        else:
            st.error("Oops! That's not quite right. Try again!")

# --- Footer ---
st.markdown("---")
st.markdown("Made with ❤️ for education | No API keys used | Unique in India")

        
