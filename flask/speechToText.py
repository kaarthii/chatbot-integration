import sounddevice as sd
import vosk 
import json

model=vosk.Model("C:/Users/karthi_d/Karthi/vosk-model-small-en-us-0.15")

def recognize_speech():
    device_index=sd.default.device[0]
    with sd.RawInputStream(samplerate=16000,channels=1,dtype='int16',device=device_index) as stream:
        print(sd.query_devices())
        print(sd.default.device)
        print("Listening...")
        rec=vosk.KaldiRecognizer(model,16000)
        while True:
            data=stream.read(4000)
            if rec.AcceptWaveform(data):
                result=json.loads(rec.Result())
                return result["text"]
