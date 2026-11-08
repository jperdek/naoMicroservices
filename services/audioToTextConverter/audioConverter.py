import whisperx
import gc
from whisperx.diarize import DiarizationPipeline

#from pydub import AudioSegment
#sound = AudioSegment.from_mp3("/path/to/file.mp3")
#sound.export("/output/path/file.wav", format="wav")

device = "cpu"
audio_file = "./audio.weba" #"audio.mp3"
batch_size = 32 # reduce if low on GPU mem
compute_type = "int8" # change to "int8" if low on GPU mem (may reduce accuracy)
model = "base" # "large-v2" # "base"
# 1. Transcribe with original whisper (batched)
model = whisperx.load_model(model, device, compute_type=compute_type, language="sk")

# save model to local path (optional)
model_dir = "./model/"
# model = whisperx.load_model("large-v2", device, compute_type=compute_type, download_root=model_dir)

audio = whisperx.load_audio(audio_file)
result = model.transcribe(audio, batch_size=batch_size)
print(result["segments"]) # before alignment

# delete model if low on GPU resources
# import gc; import torch; gc.collect(); torch.cuda.empty_cache(); del model

# 2. Align whisper output
model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)

print(result["segments"]) # after alignment
print(result)


