import os
import json
from typing import List, Dict, Optional
from time import time
import shutil

from playsound import playsound
import pandas as pd

from vad_streaming import VADAudio


DEFAULT_SAMPLE_RATE = 16000


def get_option() -> str:
    print('  [1] - Save')
    print('  [2] - Listen')
    print('  [3] - Retry')
    print('  [4] - Skip')

    answer = input('Your selection: ')

    if answer not in '1234':
        print('\033[91m{}\033[0m'.format('Unsupported command. Select one of the provided options.'))
        return get_option()

    return answer


def request_record(sentence: str, out_dir: str, vad_aggressiveness: int = 2) -> Optional[str]:
    file_path = None
    flag = True
    to_record = True

    print('Say the sentence: ', end='')
    print(f'\033[93m{sentence}\033[0m')
    
    while flag:
        if to_record:
            vad_audio = VADAudio(aggressiveness=vad_aggressiveness,
                            device=None,
                            input_rate=DEFAULT_SAMPLE_RATE)
            
            print("Listening...")
            frames = vad_audio.vad_collector()

            wav_data = bytearray()
            for frame in frames:
                if frame is not None:
                    wav_data.extend(frame)
                else:
                    break
            file_path = f'{out_dir}/{time()}.wav'
            vad_audio.write_wav(file_path, wav_data)
        else:
            playsound(file_path)

        option = get_option()
        if option == '1':
            flag = False
        elif option == '2':
            to_record = False
        elif option == '3':
            os.remove(file_path)
            to_record = True
        elif option == '4':
            file_path = None
            flag = False

    return file_path


def record(sentences: List[str], out_dir: str) -> Dict[str, List[str]]:
    d = {
        'text': [],
        'path': [],
    }

    for sentence in sentences:
        filename = request_record(sentence, out_dir)

        if filename:
            d['text'].append(sentence)
            d['path'].append(filename)

    return d


if __name__ == '__main__':
    out_dir = 'data'

    with open('texts.json', 'r') as f:
        sentences = json.load(f)
    
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    records = record(sentences, out_dir)

    df = pd.DataFrame.from_dict(records)
    df.to_csv(out_dir + '/records.tsv', sep='\t')

    print('Dataset saved.\nBye!')
