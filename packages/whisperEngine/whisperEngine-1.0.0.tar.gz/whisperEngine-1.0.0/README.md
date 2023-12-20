This is a package of the whisper engine that you can install and use 
without complicated initialization and construction processes. 

1. First you need to install the FastWhishper environment:
pip install faster-whisper


2. How to use it:

size = "large-v2" 
model = "model_path"
language = "zh"
whisper = whisperEngine(size, model, language)
whisper.load_model()
text = whisper.do_transcribe(audio_file)


3. model language default chinese:
 chinese (zh)
 english (en)