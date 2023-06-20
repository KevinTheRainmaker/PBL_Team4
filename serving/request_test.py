import requests
import argparse
import os

url = "https://mobilex.kr/ai/dev/team4/predict/inference"

parser = argparse.ArgumentParser()
parser.add_argument("--input_text", type=str, help="Input text for synthesis")
args = parser.parse_args()

# 요청 페이로드
payload = {
    "input_text": args.input_text,
    "text2mel_model": "fastspeech2",
    "vocoder_model": "mb_melgan"
}

# POST 요청 보내기
response = requests.post(url, json=payload)

# 응답 확인
if response.status_code == 200:
    data = response.json()
    # print(data)
    # quit()
    mel_outputs = data["mel_outputs"]
    audio = data["audio"]
    print("Mel outputs:", bool(mel_outputs))
    print("Audio:", bool(audio))
else:
    print("Request failed with status code:", response.status_code)
    
os.system("scp -r InferenceDE:/home/team4/Modeling/serving/app/wav_dir ./app")

