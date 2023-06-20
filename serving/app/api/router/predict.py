import tensorflow as tf
from tensorflow_tts.inference import TFAutoModel
from tensorflow_tts.inference import AutoProcessor
from scipy.io.wavfile import write
import numpy as np
from fastapi import APIRouter, Request
from pathlib import Path

physical_devices = tf.config.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

router = APIRouter(
    prefix="/ai/dev/team4/predict",
    tags=["predict"],
    responses={404: {"description": "Not Found"}},
)

fastspeech2 = TFAutoModel.from_pretrained("tensorspeech/tts-fastspeech2-kss-ko", name="fastspeech2")
mb_melgan = TFAutoModel.from_pretrained("tensorspeech/tts-mb_melgan-kss-ko", name="mb_melgan")
processor = AutoProcessor.from_pretrained("tensorspeech/tts-fastspeech2-kss-ko")

@router.post("/inference")
async def do_synthesis(request: Request):
    request_body = await request.json()
    input_text = request_body.get('input_text', '')
    # text2mel_model = request_body.get('text2mel_model', 'fastspeech2')
    # vocoder_model = request_body.get('vocoder_model', 'mb_melgan')
    text2mel_model = fastspeech2
    vocoder_model = mb_melgan

    input_ids = processor.text_to_sequence(input_text)
    # text2mel part
    _, mel_outputs, _, _, _ = text2mel_model.inference(
        tf.expand_dims(tf.convert_to_tensor(input_ids, dtype=tf.int32), 0),
        speaker_ids=tf.convert_to_tensor([0], dtype=tf.int32),
        speed_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
        f0_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
        energy_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
    )

    # vocoder part
    audio = vocoder_model.inference(mel_outputs)[0, :, 0]

    mel_outputs = mel_outputs.numpy()
    audio = audio.numpy()

    rate = 22050
    scaled = np.int16(audio / np.max(np.abs(audio)) * 32767)
    result_path = './wav_dir'
    result_path = Path(result_path)
    result_path.mkdir(parents=True, exist_ok=True)
    write(f'./wav_dir/{input_text}.wav', rate, scaled)
    
    audio = './wav_dir/{input_text}.wav'

    return {"mel_outputs": mel_outputs.tolist(), "audio": audio.tolist()}



router = APIRouter(
    prefix="/ai/dev/team4/predict",
    tags=["predict"],
    responses={404: {"description": "Not Found"}},
)

fastspeech2 = TFAutoModel.from_pretrained("tensorspeech/tts-fastspeech2-kss-ko", name="fastspeech2")
mb_melgan = TFAutoModel.from_pretrained("tensorspeech/tts-mb_melgan-kss-ko", name="mb_melgan")
processor = AutoProcessor.from_pretrained("tensorspeech/tts-fastspeech2-kss-ko")

@router.post("/inference")
async def do_synthesis(request: Request):
    request_body = await request.json()
    input_text = request_body.get('input_text', '')
    # text2mel_model = request_body.get(text2mel_model, fastspeech2)
    # vocoder_model = request_body.get(vocoder_model, mb_melgan)
    text2mel_model = fastspeech2
    vocoder_model = mb_melgan

    input_ids = processor.text_to_sequence(input_text)
    # text2mel part
    _, mel_outputs, _, _, _ = text2mel_model.inference(
        tf.expand_dims(tf.convert_to_tensor(input_ids, dtype=tf.int32), 0),
        speaker_ids=tf.convert_to_tensor([0], dtype=tf.int32),
        speed_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
        f0_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
        energy_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
    )

    # vocoder part
    audio = vocoder_model.inference(mel_outputs)[0, :, 0]

    mel_outputs = mel_outputs.numpy()
    audio = audio.numpy()

    rate = 22050
    scaled = np.int16(audio / np.max(np.abs(audio)) * 32767)
    result_path = './wav_dir'
    result_path = Path(result_path)
    result_path.mkdir(parents=True, exist_ok=True)
    write(f'./wav_dir/{input_text}.wav', rate, scaled)
    
    # audio = './wav_dir/{input_text}.wav'
    # output_file_name = create_output_file_name()
    
    # save_audio(audio, output_file_name)

    return {"mel_outputs": mel_outputs.tolist(), "audio": audio.tolist()}
