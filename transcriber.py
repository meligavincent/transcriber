import os
import time
import gradio as gr
from groq import Groq
from dotenv import load_dotenv
import tempfile
import soundfile as sf  # pip install soundfile if necessary
import requests

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# Enhanced CSS with modern design and animations
custom_css = """
:root {
    --primary-color: #6366f1;
    --bg-color: #ffffff;
    --text-color: #1f2937;
    --border-color: #e5e7eb;
    --card-bg: rgba(255, 255, 255, 0.9);
    --glass-bg: rgba(255, 255, 255, 0.1);
    --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.dark {
    --primary-color: #818cf8;
    --bg-color: #0f172a;
    --text-color: #f8fafc;
    --border-color: #334155;
    --card-bg: rgba(15, 23, 42, 0.9);
    --glass-bg: rgba(15, 23, 42, 0.1);
    --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
}

.gradio-container {
    background: var(--bg-color) !important;
    color: var(--text-color) !important;
    max-width: 1000px !important;
    margin: 20px auto !important;
    padding: 20px !important;
    border-radius: 12px !important;
}

.gradio-interface {
    backdrop-filter: blur(10px) !important;
    background: var(--glass-bg) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
    box-shadow: var(--shadow) !important;
}

.section {
    padding: 24px;
    margin: 12px 0;
    background: var(--card-bg);
    border-radius: 8px;
    border: 1px solid var(--border-color);
}

.loading-bar {
    height: 3px !important;
    background: var(--primary-color) !important;
    margin: 10px 0;
    animation: pulse 2s infinite;
}

.processing-indicator {
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
}
"""

SUPPORTED_LANGUAGES = {
    "en": "English", "es": "Spanish", "fr": "French", 
    "de": "German", "it": "Italian", "pt": "Portuguese",
    "ru": "Russian", "zh": "Chinese", "ja": "Japanese",
    "ko": "Korean", "ar": "Arabic", "hi": "Hindi"
}

def toggle_theme():
    """Toggle between light/dark themes"""
    return gr.update()

def transcribe(audio_file):
    """Transcribe audio using Whisper API with error handling"""
    if not audio_file:
        return "", "", None
    try:
        start_time = time.time()
        with open(audio_file, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(audio_file, file.read()),
                model="whisper-large-v3",
                response_format="verbose_json",
            )
        return (
            transcription.text,
            SUPPORTED_LANGUAGES.get(transcription.language, transcription.language),
            f"Processed in {time.time() - start_time:.2f}s" #| Confidence: {transcription.language_probability:.2%}"
        )
    except Exception as e:
        return "", "", f"Error: {str(e)}"

def translate_text(text, source_lang, target_lang):
    """Translate text using Groq API with enhanced prompt via model gemma2-9b-it (streaming)"""
    if not text:
        return "", None
    try:
        start_time = time.time()
        prompt = f"Translate this from {source_lang} to {target_lang} while preserving meaning and cultural nuances:\n{text}"
        messages = [
            {
                "role": "system",
                "content": "You are a professional translator. Maintain formal register unless specified otherwise."
            },
            {"role": "user", "content": prompt}
        ]
        # Création d'une complétion en mode streaming avec le modèle gemma2-9b-it
        completion = client.chat.completions.create(
            model="gemma2-9b-it",
            messages=messages,
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
        translated_chunks = []
        for chunk in completion:
            delta = chunk.choices[0].delta
            if hasattr(delta, "content") and delta.content:
                translated_chunks.append(delta.content)
        translated_text = "".join(translated_chunks).strip()
        elapsed = time.time() - start_time
        return translated_text, f"Translated in {elapsed:.2f}s using Gemma2-9B-IT"
    except Exception as e:
        return f"Translation error: {str(e)}", None


def text_to_speech(text, lang):
    """Convert text to speech using Groq API with appropriate model and voice."""
    if not text:
        print("TTS: No text input provided")
        return None, None
    
    try:
        print(f"TTS: Processing text '{text[:30]}...' in language '{lang}'")
        
        # Define the model and voice based on the language
        if lang.lower() in ["arabic", "ar"]:
            model = "playai-tts-arabic"  # Placeholder for the Groq Arabic model
            voice = "Ahmad-PlayAI"  # Placeholder for Arabic voice
        else:
            model = "playai-tts"  # Placeholder for the general Groq TTS model
            voice = "Fritz-PlayAI"  # Placeholder for the general voice
        
        # Set the desired response format (e.g., wav)
        response_format = "wav"
        
        # Send request to Groq API for text-to-speech generation
        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=text,
            response_format=response_format
        )

        # Save the response as a temporary file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_filename = tmp.name
            response.write_to_file(tmp_filename)  # This writes the audio to a temp file

        print(f"TTS: Audio file saved at {tmp_filename}")

        # Check if the file is a valid audio format and read it
        try:
            audio_data, samplerate = sf.read(tmp_filename)  # Read the audio file (wav)
        except Exception as e:
            print(f"Error reading audio file: {e}")
            return None, None

        os.remove(tmp_filename)  # Clean up temporary file

        print("TTS: Successfully processed audio")
        return audio_data, samplerate

    except Exception as e:
        print(f"TTS error: {e}")
        return None, None


def update_history(timestamp, source_lang, target_lang, preview):
    """Update history with new interaction details."""
    history.append([timestamp, source_lang, target_lang, preview])
    return history


with gr.Blocks(css=custom_css, theme=gr.themes.Default()) as demo:
    # State management
    history = gr.State([])

    # Header with theme toggle
    with gr.Row(variant="compact"):
        gr.Markdown("# 🌐 Next-Gen Audio Translator", elem_classes="gradio-interface")
        theme_btn = gr.Button("🌙", elem_id="theme_btn")

    # Indicator de chargement
    with gr.Column(visible=False) as processing_indicator:
        gr.Markdown("Analyzing content...", elem_classes="processing-indicator")
        gr.Markdown('<div class="loading-bar"></div>', elem_classes="loading-bar")

    # Section Input
    gr.Markdown("## 📤 Input", elem_classes="gradio-interface")
    with gr.Column(elem_classes="section"):
        audio_input = gr.Audio(
            sources=["microphone", "upload"],
            type="filepath",
            label="Audio Input",
            waveform_options={"show_controls": True},
            interactive=True
        )
        with gr.Row():
            transcribe_btn = gr.Button("Transcribe", variant="primary")
            realtime_toggle = gr.Checkbox(label="Real-time Processing", interactive=True)

    # Section Results
    gr.Markdown("## 📝 Results", elem_classes="gradio-interface")
    with gr.Column(elem_classes="section"):
        with gr.Row():
            with gr.Column(scale=2):
                transcribed_text = gr.Textbox(
                    label="Original Transcription",
                    lines=5,
                    interactive=True
                )
                detected_lang = gr.Textbox(
                    label="Detected Language",
                    interactive=False
                )
                lang_confidence = gr.Textbox(
                    label="Analysis Details",
                    interactive=False
                )
            with gr.Column(scale=1):
                gr.Markdown("### Translation Settings")
                target_lang = gr.Dropdown(
                    label="Target Language",
                    choices=list(SUPPORTED_LANGUAGES.values()),
                    value="English"
                )
                translate_btn = gr.Button("Translate", variant="primary")
                tts_btn = gr.Button("🔊 Play Translation")
        translated_text = gr.Textbox(
            label="Translated Text",
            lines=5,
            interactive=False
        )
        translation_details = gr.Textbox(
            label="Translation Details",
            interactive=False
        )
        audio_output = gr.Audio(label="Speech Output", visible=False)

    # Section History
    gr.Markdown("## 📚 History", elem_classes="gradio-interface")
    with gr.Column(elem_classes="section"):
        history_table = gr.DataFrame(
            headers=["Timestamp", "Source Language", "Target Language", "Preview"],
            interactive=False
        )
        clear_history_btn = gr.Button("Clear History")

    # Theme toggle functionality
    theme_btn.click(
        fn=None,
        js="""() => {
            document.querySelector('.gradio-container').classList.toggle('dark');
            const btn = document.querySelector('#theme_btn');
            btn.textContent = btn.textContent === '🌙' ? '☀️' : '🌙';
            document.dispatchEvent(new Event('theme-change'));
        }""",
    )

    # Interactive workflow
    transcribe_btn.click(
        lambda: (gr.update(visible=True), None, processing_indicator)
    ).then(
        transcribe, audio_input, [transcribed_text, detected_lang, lang_confidence]
    ).then(
        lambda: gr.update(visible=False), None, processing_indicator
    )

    translate_btn.click(
        lambda: (gr.update(visible=True), gr.update(visible=False)),
        None, [processing_indicator, audio_output]
    ).then(
        translate_text, [transcribed_text, detected_lang, target_lang], [translated_text, translation_details]
    ).then(
        lambda: gr.update(visible=False), None, processing_indicator
    )

    tts_btn.click(
        text_to_speech, [translated_text, target_lang], audio_output
    ).then(
        lambda: gr.update(visible=True), None, audio_output
    )

    # History management
    clear_history_btn.click(lambda: [], None, history)
    
    demo.load(
        lambda h: h if h else [],
        history, history_table
    )

demo.launch(
    server_name="0.0.0.0" if os.getenv("DOCKER") else "127.0.0.1",
    share=os.getenv("SHARE", False)
)
