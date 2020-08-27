import os
from shutil import rmtree 
from glob import glob as glb
from pydub import AudioSegment
from pydub.silence import split_on_silence
#import speech_recognition as sr
from speech_recognition import Recognizer,AudioFile,UnknownValueError
r = Recognizer()

def get_large_audio_transcription(path,k,total):
    Time=[]
    time_=0
    srt_=[]
    sound = AudioSegment.from_wav(path)  
    chunks = split_on_silence(sound,
        min_silence_len = 500,
        silence_thresh = sound.dBFS-14,
        keep_silence=500)
    folder_name = "audio-chunks"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    j=0
    length=len(chunks)
    for i, audio_chunk in enumerate(chunks, start=1):
        
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        
        dur=audio_chunk.duration_seconds
        Time.append([i,round(time_,3),round(time_+dur,3)])
        time_+=dur
        
        with AudioFile(chunk_filename) as source:
            j+=1
            audio_listened = r.record(source)
            try:
                text = r.recognize_google(audio_listened)
            except UnknownValueError as e:
                print("Error:CAN NOT RECOGNIZE SPEECH!", str(e))
                srt_.append("")
            else:
                text = f"{text.capitalize()}. "
                print('/ file %s from %s \ '%(k+1,total),end='')
                print('/ chunk %d:%d \\'%(j,length),end='')
                if len(text)>40:
                    print( ":", text[:40]+'...')
                else:
                    print(":", text)
                whole_text += text+'\n'
                srt_.append(text)
    return whole_text,Time,srt_

def mytime(end):
    hour=int((end/60)/60)
    end-=hour*60
    hour='0'+str(hour) 
    minute=int(end/60)
    end-=minute*60
    if minute<10:
        minute='0'+str(minute)
    else:
        minute=str(minute)   
    sec=int(end)
    sec_=str(round(end-sec,3))
    sec_=sec_[2:]
    if sec<10:
        sec='0'+str(sec)+','+sec_
    else:
        sec=str(sec)+','+sec_
    
    end_=hour+':'+minute+':'+sec
    return end_




File=[]
for file in glb("*.mp3"):
    File.append(file)
total=len(File)
print(str(total)+' mp3 file is found \n starting the process : \n')

if not os.path.isdir('output'):
    os.mkdir('output')
for k,src in enumerate(File):
    


    dst = "test.wav"

    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")


    wholetext,time,raw=get_large_audio_transcription(dst,k,total)

    sub=''
    for i,row in enumerate(time):
        try:
            txt=str(row[0])+'\n'
            
            start=row[1]
            end=row[2]
            
            b1=mytime(start)
            b2=mytime(end)
            txt+=b1+' --> '+b2+'\n'
            txt+=raw[i]+'\n\n'
            sub+=txt
        except:
            pass
    name=src[:-4]
    
    fop=open('output\\'+name+'.srt','w')
    fop.write(sub)
    fop.close()

    fop=open('output\\'+name+'.txt','w')
    fop.write(wholetext)
    fop.close()

    rmtree('audio-chunks')
    os.remove('test.wav')
    
print('\n\n Done!')