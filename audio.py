import threading
from array import array
from queue import Queue, Full
import wave, os, io

import pyaudio
import dialogflow_v2 as dialogflow
import uuid
import json
from robomover import RoboMover


CHUNK_SIZE = 8192
MIN_VOLUME = 100
# if the recording thread can't consume fast enough, the listener will start discarding
BUF_MAX_SIZE = CHUNK_SIZE * 20
MAX_SILENCES = 4
CHANNELS = 1
RATE = 44100
FORMAT = pyaudio.paInt16


WAVE_OUTPUT_FILENAME = "file"
mover = RoboMover()

# [START dialogflow_detect_intent_audio]
def detect_intent_audio(session_id, input_audio_stream):
    """Returns the result of detect intent with an audio file as input.
    Using the same `session_id` between requests allows continuation
    of the conversation."""

    project_id = "piworkout"
    language_code = 'en-US'
    session_client = dialogflow.SessionsClient()
    input_audio = input_audio_stream.read()

    # Note: hard coding audio_encoding and sample_rate_hertz for simplicity.
    audio_encoding = dialogflow.enums.AudioEncoding.AUDIO_ENCODING_LINEAR_16
    sample_rate_hertz = RATE

    session = session_client.session_path(project_id, session_id)
    #print('Session path: {}\n'.format(session))

    #with open(audio_file_path, 'rb') as audio_file:
    #    input_audio = audio_file.read()

    audio_config = dialogflow.types.InputAudioConfig(
        audio_encoding=audio_encoding, language_code=language_code,
        sample_rate_hertz=sample_rate_hertz)
    query_input = dialogflow.types.QueryInput(audio_config=audio_config)

    response = session_client.detect_intent(
        session=session, query_input=query_input,
        input_audio=input_audio)
    input_audio_stream.close()

    print('=' * 20)
    #print('Query text: {}'.format(response.query_result.query_text))
    #print('Detected intent: {} (confidence: {})\n'.format(
    #    response.query_result.intent.display_name,
    #    response.query_result.intent_detection_confidence))
    print('response: {}\n'.format(
        response.query_result.fulfillment_text))
    
    command = dict()
    try:
        command = json.loads(response.query_result.fulfillment_text)
        print(command)
        
    except:
        print("invalid command" + response.query_result.fulfillment_text)
        pass  # discard
# [END dialogflow_detect_intent_audio]

    if "action" in command:
        
        speed = "slow"
        if "speed" in command:
            speed = command["speed"]
        mover.Move(command["action"], command["direction"], speed)


def main():
    stopped = threading.Event()
    q = Queue(maxsize=int(round(BUF_MAX_SIZE / CHUNK_SIZE)))

    listen_t = threading.Thread(target=listen, args=(stopped, q))
    listen_t.start()
    record_t = threading.Thread(target=record, args=(stopped, q))
    record_t.start()

    try:
        while True:
            listen_t.join(0.1)
            record_t.join(0.1)
    except KeyboardInterrupt:
        stopped.set()

    listen_t.join()
    record_t.join()
    mover.Done()


def record(stopped, q):
    frames = []
    file_count = 1
    silences = MAX_SILENCES
    voice_detected = True
    while True:
        if stopped.wait(timeout=0):
            break
        chunk = q.get()
        vol = max(chunk)
        print(vol)
        if vol >= MIN_VOLUME:
            frames.append(chunk)
            voice_detected = True
            silences = MAX_SILENCES
        else:
            if(silences > 0):
                silences = silences -1
                frames.append(chunk)
            if(silences <= 0) and voice_detected:
                audio_stream = b''.join(frames)
                memstream = io.BytesIO()
                waveFile = wave.open(memstream, 'wb')
                waveFile.setnchannels(CHANNELS)
                waveFile.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
                waveFile.setframerate(RATE)
                waveFile.writeframes(audio_stream)
                waveFile.close()
                memstream.seek(0)
                detect_intent_thread = threading.Thread(target=detect_intent_audio, args=(str(uuid.uuid4()), memstream))
                detect_intent_thread.start()
                frames = []
                file_count = file_count + 1
                silences = MAX_SILENCES
                voice_detected = False


def listen(stopped, q):
    stream = pyaudio.PyAudio().open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE,
    )

    while True:
        if stopped.wait(timeout=0):
            break
        try:
            q.put(array('h', stream.read(CHUNK_SIZE)))
        except Full:
            pass  # discard


if __name__ == '__main__':
    main()
