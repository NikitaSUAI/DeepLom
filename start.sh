cde .
echo "Start"
echo "Make noise"
#for audio in Audio/*; do
#	python3 make_noise.py $audio 	
#	python3 make_noise.py $audio 10
#	python3 make_noise.py $audio 5
#done

#echo "chande duration"
#for audio in Audio/*; do
#	python3 change_duration.py $audio 
#	python3 change_duration.py $audio 3
#done

echo "preprocessing done"
cde -e

#--pyannote audio---------------->
#echo "pyannote-audio"
#cde pyannote-audio
#echo "go to pyanno"
#for audio in ../Audio/*; do
#	echo "diar $audio";
#	python3 main.py $audio;
#done
#cde ..

#--pyBK-------------------------->
#echo "pyBK"
#cp Audio/* pyBK/audio/

#cde pyBK
#python3 main.py
#cde ..

#--pyAudioAnalysis--------------->
echo "pyAudioAnalysis"
cde pyAudioAnalysis
for audio in ../Audio/*;do
	echo "pyAudioAnalysis on $audio"
	python3 main.py $audio MixHeadset.test.rttm
done;
cde ..
cde -e
echo "done"
