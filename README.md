# Next-Gen Audio Translator

A cutting-edge audio translation tool that transcribes spoken language, translates it to your desired language, and converts the translation back to speech. Built with Python, [Gradio](https://gradio.app/) for an interactive web interface, and powered by the Groq API for transcription, translation, and text-to-speech functionality.

---

[![Watch the demo video](https://img.youtube.com/vi/JSHGy0kh9_Q/maxresdefault.jpg)](https://youtu.be/JSHGy0kh9_Q)

---

## Overview

The Next-Gen Audio Translator is designed to offer a seamless experience for users who need to convert audio content across languages. Key functionalities include:

- **Audio Transcription:** Uses a Whisper-based model (`whisper-large-v3`) to transcribe input audio.
- **Language Detection:** Automatically detects and displays the source language.
- **Translation:** Leverages the Groq API with the `gemma2-9b-it` model to translate text, preserving meaning and cultural nuances.
- **Text-to-Speech (TTS):** Converts the translated text back into audio using dedicated TTS models (with support for language-specific voices).
- **Modern UI:** Features an interactive Gradio interface with customizable themes, responsive design, and history tracking.
- **Real-time Processing:** Option for real-time transcription and translation with an animated loading indicator.

---

## Features

- **Multiple Languages:** Supports transcription and translation in languages including English, Spanish, French, German, Italian, Portuguese, Russian, Chinese, Japanese, Korean, Arabic, and Hindi.
- **Theme Toggle:** Easily switch between light and dark modes with a simple button click.
- **Responsive Design:** Custom CSS with modern design and subtle animations for an enhanced user experience.
- **History Tracking:** Maintains a record of interactions (timestamps, source/target languages, and preview text) for quick reference.
- **Error Handling:** Robust error management for smoother operation during audio processing and API interactions.

---

## Installation

### Prerequisites

- **Python 3.12+**
- Required Python packages:
  - `gradio`
  - `groq`
  - `python-dotenv`
  - `soundfile`
  - `requests`

You can install the dependencies using `pip`:

```bash
pip install gradio groq python-dotenv soundfile requests
```

### Environment Variables

Create a `.env` file in your project directory and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Replace `your_groq_api_key_here` with your actual API key from Groq.

---

## Usage

### Running the Application

To launch the Next-Gen Audio Translator, simply run the Python script:

```bash
python transcriber.py
```

The application will start a local web server (by default on `127.0.0.1:7860` or another port if configured) and automatically open the Gradio interface in your web browser.

### Interacting with the Interface

1. **Audio Input:** Use the microphone or upload an audio file.
2. **Transcription:** Click the **Transcribe** button to convert speech to text.
3. **Translation:** Select your target language from the dropdown and click **Translate**.
4. **Text-to-Speech:** Click the **🔊 Play Translation** button to hear the translated text.
5. **History:** View past interactions in the history section or clear the history as needed.
6. **Theme Toggle:** Switch between light and dark themes using the theme button in the header.

---

## Configuration

### Custom CSS

The project includes a custom CSS block that:
- Defines primary, background, text, and border colors.
- Applies a glass effect to interface components.
- Implements subtle animations (e.g., loading indicators and theme transitions).

Feel free to modify the `custom_css` variable to tailor the interface design to your preferences.

### API Integration

- **Transcription:** Uses Groq's audio transcription endpoint with the `whisper-large-v3` model.
- **Translation:** Utilizes a streaming chat completion with the `gemma2-9b-it` model to ensure natural and accurate translations.
- **Text-to-Speech:** Adjusts models and voices based on the target language. The example includes placeholders for Arabic and a general TTS model.

---

## Contributing

Contributions are welcome! If you have suggestions or improvements, please feel free to submit a pull request or open an issue on the repository.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- **Gradio:** For providing an excellent framework to build interactive web apps.
- **Groq API:** For powering the transcription, translation, and TTS features.
- **Whisper:** For the robust transcription model that drives the audio-to-text functionality.

---