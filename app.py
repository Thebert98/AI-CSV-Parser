import streamlit as st
from langchain_experimental.agents import create_csv_agent
from langchain_openai import ChatOpenAI
from openai import OpenAI
from pydub import AudioSegment
from langchain_groq import ChatGroq
import simpleaudio as sa
from pathlib import Path
from dotenv import load_dotenv
import sounddevice as sd
from scipy.io.wavfile import write

# Load environment variables from a .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

def use_mic():
    """
    Records audio from the microphone, saves it as a WAV file,
    transcribes it using OpenAI's Whisper model, and returns the transcript.
    """
    fs = 44100  # Sample rate
    seconds = 4  # Duration of recording

    # Record audio
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    write('output.wav', fs, myrecording)  # Save as WAV file

    # Transcribe audio
    with open("output.wav", "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
    
    return transcript

def main():
    # Set up the Streamlit page
    st.set_page_config(page_title="CSV Parser")
    st.header("Ask The CSV", divider="green")

    # File uploader for CSV file
    user_csv = st.file_uploader("Upload your CSV file", type="csv")

    if user_csv is not None:
        # LLM provider selection
        option = st.selectbox(
            "Choose what LLM to use",
            ("OpenAI", "Groq"),
            index=None,
            placeholder="Select an LLM provider..."
        )

        if option:
            # Input mode selection for OpenAI
            if option == "OpenAI":
                mode = st.selectbox(
                    "Choose an input mode",
                    ("Text", "Voice"),
                    index=None,
                    placeholder="Select input mode..."
                )

                if mode == "Voice":
                    if st.button("Record Question"):
                        
                        # Record and transcribe question
                        transcript = use_mic()
                        st.write(f"Your Question: {transcript}")

                        # Initialize OpenAI LLM and CSV agent
                        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
                        agent = create_csv_agent(llm, user_csv, handle_parsing_errors=True,verbose=True)

                        if transcript:
                            response = agent.run(transcript)
                            st.write(response)
                            st.write("The answer will be read to you shortly using text-to-speech.")

                            # Convert response to speech
                            speech_file_path = Path(__file__).parent / "speech.mp3"
                            response_audio = client.audio.speech.create(
                                model="tts-1",
                                voice="fable",
                                input=response
                            )
                            response_audio.stream_to_file(speech_file_path)

                            sound = AudioSegment.from_mp3(speech_file_path)
                            sound.export("speech.wav", format="wav")

                            # Play the speech
                            wave_object = sa.WaveObject.from_wave_file("speech.wav")
                            play_obj = wave_object.play()
                            play_obj.wait_done()

                elif mode == "Text":
                    # Text input mode
                    user_question = st.text_input("Ask a question to the CSV:")
                    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
                    agent = create_csv_agent(llm, user_csv, verbose=True,handle_parsing_errors=True)

                    if user_question:
                        response = agent.run(user_question)
                        st.write(response)

            elif option == "Groq":
                # Groq LLM provider
                user_question = st.text_input("Ask a question to the CSV:")
                llm = ChatGroq(temperature=0, model_name="gemma2-9b-it")
                agent = create_csv_agent(llm, user_csv, verbose=True,handle_parsing_errors=True)

                if user_question:
                    response = agent.run(user_question)
                    st.write(response)

# Run the main function
if __name__ == "__main__":
    main()
