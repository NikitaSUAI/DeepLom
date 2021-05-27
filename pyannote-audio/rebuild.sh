cde -e;
rm -r env;
python3.7 -m venv env
cde .
pip install --upgrade pip
pip install jupyterlab
pip install tensorflow==2.4.1
pip install torch==1.8.1+cpu torchvision==0.9.1+cpu torchaudio==0.8.1 -f https://download.pytorch.org/whl/torch_stable.html
pip install librosa
pip install pyyaml
pip install pyannote.audio==1.1.1
python3 -c "import torch;torch.hub.load('pyannote/pyannote-audio', 'dia')"
