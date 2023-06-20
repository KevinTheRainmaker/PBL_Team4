import datetime
import json
import os
import time
from datetime import datetime
from io import BytesIO

import requests
from django.test import TestCase

from core.print import print_colored
from core.setup import BUCKET_NAME, openai, s3
from core.utility import (add_assistant_message_to_messages,
                          add_user_message_to_messages,
                          create_output_file_name, decode_audio, generate_text,
                          get_audio_file_url_using_polly,
                          get_complete_message_by_chatgpt, get_file_url,
                          get_sentences_by_chatgpt, has_special_characters,
                          save_audio, save_file_to_s3)

print_colored(f"BUCKET_NAME: {BUCKET_NAME}", "red")

TEST_INPUT_JSON_PATH = "core/tests/src/test_input.json"
TEST_FILE_PATH = "core/tests/src/test.txt"


def check_file_in_s3_bucket(bucket_name, file_key):
    try:
        s3.head_object(Bucket=bucket_name, Key=file_key)
        print(f"File '{file_key}' exists in bucket '{bucket_name}'.", "blue")
        return True
    except s3.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            print_colored(
                f"File '{file_key}' not found in bucket '{bucket_name}'.", "yellow")
        else:
            print_colored(
                f"Error checking file '{file_key}' in bucket '{bucket_name}': {e}", "red")
        return False


class CoreUtilityTest(TestCase):

    def test_get_file_url(self):
        with open(TEST_FILE_PATH, 'rb') as f:
            content = f.read()
        test_file = BytesIO(content)
        test_file.name = "test.txt"
        try:
            s3.delete_object(Bucket=BUCKET_NAME, Key=test_file.name)
        except Exception as e:
            print(e)
        save_file_to_s3(test_file, test_file.name)
        response = requests.get(get_file_url(test_file.name))

        assert response.status_code == 200

        s3.delete_object(Bucket=BUCKET_NAME, Key=test_file.name)

    def test_save_file_to_s3(self):
        with open(TEST_FILE_PATH, 'rb') as f:
            content = f.read()
        test_file = BytesIO(content)
        test_file.name = "test.txt"
        try:
            s3.delete_object(Bucket=BUCKET_NAME, Key=test_file.name)
        except Exception as e:
            print(e)
        save_file_to_s3(test_file, test_file.name)
        assert check_file_in_s3_bucket(BUCKET_NAME, test_file.name)

        s3.delete_object(Bucket=BUCKET_NAME, Key=test_file.name)

    def test_decode_audio(self):
        with open(TEST_INPUT_JSON_PATH, 'r') as f:
            json_data = json.load(f)
        audio_data = decode_audio(json_data["audio"])
        audio_file = BytesIO(audio_data)
        audio_file.name = f'test_input.mp3'
        now_second = datetime.now().second
        test_output_name = f"core/tests/src/test_output_{now_second}.mp3"
        with open(test_output_name, "wb") as f:
            f.write(audio_data)
        assert os.path.exists(
            test_output_name), f"The file '{test_output_name}' does not exist"
        os.remove(test_output_name)

    def test_save_audio(self):
        with open(TEST_INPUT_JSON_PATH, 'r') as f:
            json_data = json.load(f)
        audio_data = decode_audio(json_data["audio"])
        test_file_name = create_output_file_name()
        save_audio(audio_data, test_file_name)
        assert check_file_in_s3_bucket(BUCKET_NAME, test_file_name)
        s3.delete_object(Bucket=BUCKET_NAME, Key=test_file_name)

    def test_generate_text(self):
        with open(TEST_INPUT_JSON_PATH, 'r') as f:
            json_data = json.load(f)
        audio_data = decode_audio(json_data["audio"])
        start_time = time.time()
        text = generate_text(audio_data)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print_colored("Generate Text By Audio Time elapsed: {:.2f} seconds".format(
            elapsed_time), "blue")
        assert "안녕하세요" in text

    def test_add_user_message_to_messages(self):
        existing_messages = [
            {"role": "system", "content": "This is just test"},
            {"role": "user", "content": "Hello World?!"},
            {"role": "assistant", "content": "GoodBye World!"}
        ]
        new_message = "Hello World! Again!"
        result_messages = add_user_message_to_messages(
            existing_messages, new_message)
        assert len(result_messages) == 4
        assert result_messages[3]["role"] == "user"
        assert result_messages[3]["content"] == new_message

    def test_add_assistant_message_to_messages(self):
        existing_messages = [
            {"role": "system", "content": "This is just test"},
            {"role": "user", "content": "Hello World?!"},
        ]
        new_message = "GoodBye World!"
        result_messages = add_assistant_message_to_messages(
            existing_messages, new_message)
        assert len(result_messages) == 3
        assert result_messages[2]["role"] == "assistant"
        assert result_messages[2]["content"] == new_message

    def test_get_complete_message_by_chatgpt(self):
        test_quote = "Hello world!"
        start_time = time.time()
        send_messages = [
            {"role": "user", "content": f"THIS IS API_TEST! You must tell me '{test_quote}'"}]
        received_message = get_complete_message_by_chatgpt(send_messages)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print_colored("Generate Text By CHATGPT elapsed: {:.2f} seconds".format(
            elapsed_time), "blue")
        assert received_message == test_quote

    def test_has_special_characters(self):
        true_test_strings = ["Hello world.",
                             "Hello world\n", "Hello world?", "Hello world!", "Hello World:"]
        false_test_strings = ["Hello world",]
        for string in true_test_strings:
            assert has_special_characters(string)
        for string in false_test_strings:
            assert not has_special_characters(string)

    def test_get_sentences_by_chatgpt(self):
        test_quote = "Give me only two sentences. And plz don'y start with numbers. Just start with english."
        start_time = time.time()
        send_messages = [
            {"role": "user", "content": f"'{test_quote}'"}]
        sentences = []
        print("START PRINT SENTENCES")
        sentence_number = 0
        for sentence in get_sentences_by_chatgpt(send_messages):
            sentences.append(sentence)
            print_colored(f"SENTENCE: {sentence}", 'green')
            assert (has_special_characters(sentence))
            sentence_number += 1
        end_time = time.time()
        elapsed_time = end_time - start_time
        print_colored(
            f"Generate {sentence_number} Sentences By CHATGPT elapsed: {elapsed_time:.2f} seconds", "blue")
        # assert received_message == test_quote

    def test_get_audio_file_url_using_polly(self):
        message = "안녕하세요"
        start_time = time.time()
        test_file_name = create_output_file_name()
        url = get_audio_file_url_using_polly(message)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print_colored("Generate AUDIO By POllY elapsed: {:.2f} seconds".format(
            elapsed_time), "blue")
        assert check_file_in_s3_bucket(BUCKET_NAME, test_file_name)
        print(
            f"GENERATED AUDIO File by POLLY URL: {url}\n(!!!!Deleted Very After Text!!!!)")
        s3.delete_object(Bucket=BUCKET_NAME, Key=test_file_name)
