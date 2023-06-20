import base64
import datetime
import time
from io import BytesIO

from core.print import print_colored
from core.setup import (AWS_S3_REGION_NAME, BUCKET_NAME, logger, openai, polly,
                        polly_voice, s3)


def get_file_url(file_key):
    return f"https://{BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/{file_key}"


def save_file_to_s3(file, file_name):
    """Return URL of file"""
    try:
        s3.upload_fileobj(file, BUCKET_NAME, file_name)
        return get_file_url(file_name)
    except Exception as e:
        raise Exception(f"Error uploading to S3: {e}")


def decode_audio(encoded_audio_data):
    audio_data = base64.b64decode(encoded_audio_data)
    return audio_data


def create_file_time():
    now = datetime.datetime.now()
    return f'{now.year}_{now.month}_{now.day}_{now.hour}{now.minute}{now.second}.wav'


def create_input_file_name():
    return f"audio/INPUT_{create_file_time()}"


def create_output_file_name():
    return f"audio/OUTPUT_{create_file_time()}"


def save_audio(audio_data, file_name):
    """Return URL of file"""
    audio_file = BytesIO(audio_data)
    try:
        return save_file_to_s3(audio_file, file_name)
    except Exception as e:
        raise Exception("An Error Occur in SAVE AUDIO")


def generate_text(audio_data):
    now = datetime.datetime.now()
    audio_file = BytesIO(audio_data)
    # 의미없다
    audio_file.name = f"audio/temp_{now.year}_{now.month}_{now.day}_{now.hour}{now.minute}{now.second}.wav"
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    text = transcript['text']
    logger.info(text)
    return text


def add_user_message_to_messages(messages, message):
    messages.append({"role": "user", "content": message})
    return messages


def add_assistant_message_to_messages(messages, message):
    messages.append({"role": "assistant", "content": message})
    return messages


def get_complete_message_by_chatgpt(messages):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages)
    return completion.choices[0].message.content.strip()


special_characters = [".", "\n", "?", "!", ":"]


def has_special_characters(string):
    for char in special_characters:
        if char in string:
            return True
    return False


def get_sentences_by_chatgpt(messages):
    response_stream = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages, stream=True)

    collected_chunks = []
    collected_messages = []
    messages_for_sentence = []
    start_time = time.time()
    for chunk in response_stream:
        collected_chunks.append(chunk)
        # print(chunk["choices"][0])
        chunk_message = chunk["choices"][0]["delta"].get('content', '')
        stop = chunk['choices'][0]['finish_reason'] == "stop"
        collected_messages.append(chunk_message)
        messages_for_sentence.append(chunk_message)
        if stop:
            break
        if has_special_characters(chunk_message):
            # print("SPECIAL_CHARACTERS: ", chunk_message)
            sentence = ''.join(
                [message for message in messages_for_sentence]).strip()
            messages_for_sentence = []
            end_time = time.time()
            elapsed_time = end_time - start_time
            print_colored("Generate SENTENCE By CHATGPT elapsed: {:.2f} seconds".format(
                elapsed_time), "blue")
            start_time = end_time
            yield sentence


def get_audio_file_url_using_polly(message):
    response = polly.synthesize_speech(
        Text=message, VoiceId=polly_voice, OutputFormat="mp3")
    audio_binary_data = response["AudioStream"].read()
    output_file_name = create_output_file_name()
    save_audio(audio_binary_data, output_file_name)
    url = s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": BUCKET_NAME, "Key": output_file_name},
        ExpiresIn=3600,
    )
    return url
