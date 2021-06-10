for rttm in ../pyannote-audio/out/*; do
  python3 myutil.py $rttm pyannote-audio
done;

for rttm in ../pyBK/out/*; do
  python3 myutil.py $rttm pyBK
done;

for rttm in ../pyAudioAnalysis/out/*; do
  python3 myutil.py $rttm pyAudioAnalysis
done;

for rttm in real/rttm/*; do
	python3 myutil.py $rttm real
done;
