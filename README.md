# Project Overview

This project, developed by Timothy Hebert, leverages the power of AI and environmental variables to manipulate and analyze data. It is designed to provide users with insights into various datasets, including CSV files, and integrates with OpenAI and GROQ APIs for enhanced data processing capabilities. The latest version includes speech-to-text and text-to-speech functionality for the OpenAI mode, enabling more interactive and user-friendly data querying.

## Features

- **CSV File Analysis**: Upload and analyze CSV files using advanced AI models.
- **OpenAI and GROQ Integration**: Choose between OpenAI and GROQ models for data processing.
- **Voice Input**: Record questions via microphone and transcribe them using OpenAI's Whisper model.
- **Text-to-Speech**: Convert AI responses to speech for an immersive user experience.

## How to Run

1. **Ensure you have Python installed on your machine.**
2. **Install the required dependencies:**
   - Run the following command in your terminal to install the required Python packages:
     ```sh
     pip install -r requirements.txt
     ```
   - Install the `ffmpeg` library using Homebrew:
     ```sh
     brew install ffmpeg
     ```
3. **Set Up Environment Variables**: 
    - Copy the example environment file to create your `.env` file:
      ```sh
      cp .env.example .env
      ```
    - Open the `.env` file and insert your OpenAI and GROQ API keys.

4. **Start the Project**:
    - Run the main script using Streamlit:
      ```sh
      streamlit run main.py
      ```
    - This will launch the web interface where you can upload CSV files, choose the LLM provider, and interact with the data.

## Usage

1. **Upload CSV File**: On the web interface, use the file uploader to select your CSV file.
2. **Select LLM Provider**: Choose between OpenAI and GROQ for data processing.
3. **Input Mode (OpenAI Only)**: 
    - Select "Text" to type your question.
    - Select "Voice" to record your question using the microphone.
4. **Get Responses**: The AI will process your question and provide a response. For voice input, the response will also be converted to speech.

## Security

- Ensure your `.env` file is added to `.gitignore` to keep your API keys secure.

## Contact

- For any inquiries or support, please contact Timothy Hebert.

---

Enjoy exploring and analyzing your data with AI-powered insights!