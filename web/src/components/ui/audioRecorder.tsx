
import ReactDOM from "react-dom/client";
import React, { useState } from "react";

import { Recorder } from 'react-voice-recorder';
import 'react-voice-recorder/dist/index.css';
import {CustomAudioPlayer} from './customAudioPlayer';



export function AudioRecorderComponent() {
    const [inputList, setInputList] = useState<{id: string, data: any}[]>([]);
    let index = 0;


    /**
     * Appends two ArrayBuffers into a new one.
     * 
     * @param {ArrayBuffer} buffer1 The first buffer.
     * @param {ArrayBuffer} buffer2 The second buffer.
     */
    function appendBuffer(buffer1, buffer2) {
        const audioCtx = new AudioContext();
        var numberOfChannels = Math.min( buffer1.numberOfChannels, buffer2.numberOfChannels );
        var tmp = audioCtx.createBuffer( numberOfChannels, (buffer1.length + buffer2.length), buffer1.sampleRate );
        for (var i=0; i<numberOfChannels; i++) {
        var channel = tmp.getChannelData(i);
        channel.set( buffer1.getChannelData(i), 0);
        channel.set( buffer2.getChannelData(i), buffer1.length);
        }
        return tmp;
    }

    async function audioBufferToWebMBlob(audioContext, audioBuffer) {
        return new Promise((resolve, reject) => {
            // 1. Create a media stream destination node
            const destination = audioContext.createMediaStreamDestination();
            
            // 2. Play the audio buffer into that destination stream
            const source = audioContext.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(destination);
            
            // 3. Set up the MediaRecorder targeting WebM / Opus
            const options = { mimeType: 'audio/webm;codecs=opus' };
            const mediaRecorder = new MediaRecorder(destination.stream, options);
            const chunks = [];
            
            // Gather WebM chunks as they become available
            mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                chunks.push(event.data);
            }
            };
            
            // When the recorder stops, bundle the chunks into a WebM Blob
            mediaRecorder.onstop = () => {
            const webmBlob = new Blob(chunks, { type: 'audio/webm;codecs=opus' });
            resolve(webmBlob);
            };
            
            mediaRecorder.onerror = (err) => reject(err);
            
            // 4. Start recording and playback simultaneously
            mediaRecorder.start();
            source.start(0);
            
            // Stop recording automatically when the audio track ends
            source.onended = () => {
            mediaRecorder.stop();
            };
        });
        }

    //chunks cannot be processed - for example to determine duration
    function handleAudioStop(data, index): void {
        const newElement = {id: index, data:<CustomAudioPlayer url={data.url} key={index} blob={data.blob} />};
        console.log(data);
        console.log(index);

        
        
        setInputList(inputList => [...inputList, newElement]);
        inputList.push(newElement);

         const audioContext = new AudioContext();
         let concatenatedBuffer = null;
         let inputElement = newElement;
         console.log(inputList.length);
        for(let j=0; j<inputList.length; j++) {
            console.log(inputList[j]);
             inputList[j].data.props.blob.arrayBuffer()
            .then((arrayBuffer) => {
                console.log("HERE");
                const AudioContext = window.AudioContext || window.webkitAudioContext;
                const audioCtx = new AudioContext();
                audioCtx.decodeAudioData(arrayBuffer).then((result) => {
                    console.log(result);
                    if (concatenatedBuffer === null) {
                        concatenatedBuffer = result;
                    } else {
                        concatenatedBuffer = appendBuffer(concatenatedBuffer, result);
                        console.log(concatenatedBuffer);
                        //const blob = audiobufferToBlob(concatenatedBuffer)
                        audioBufferToWebMBlob(audioCtx, concatenatedBuffer).then((blob) => {
                            //const blob = new Blob([concatenatedBuffer], { "type": "audio/webm;codecs=opus" });
                            const url = window.URL.createObjectURL(blob);
                            inputElement = {id: index, data:<CustomAudioPlayer url={url} key={index + 1} blob={blob} />};

                            if (inputList.length > 1 && j === inputList.length - 1) {
                                console.log("DONNNNNNNNNNNNNNNNNNNNNNNNNNNNEEE");
                                setInputList(inputList => [...inputList, inputElement]);
                                inputList.push(newElement);
                            }
                        });
                    }
                }, (e) => {console.log(e);});
           }).then((result) => { console.log(result);}, (e) => {console.log(e);});
        }
        

        handleReset();
    }

    function handleAudioUpload(file): void {
         console.log(file);
    }

    function handleCountDown(data): void {
        console.log(data);
    }

    function handleReset(): void {
        const reset = {
        url: null,
        blob: null,
        chunks: null,
        duration: {
            h: 0,
            m: 0,
            s: 0
        }
        };
    }


    const state = {
        audioDetails: {
            url: null,
            blob: null,
            chunks: null,
            duration: {
            h: 0,
            m: 0,
            s: 0
            }
        }
    }
    const rows = [];
    for (let i=0; i<inputList.length; i++) { rows.push(inputList[i].data); }
    return (
        <div>
            <Recorder
                record={true}
                title={"New recording"}
                audioURL={state.audioDetails.url}
                showUIAudio
                handleAudioStop={data => {handleAudioStop(data, index); index += 1; }}
                handleAudioUpload={data => handleAudioUpload(data)}
                handleCountDown={data => handleCountDown(data)}
                handleReset={() => handleReset()}
                mimeTypeToUseWhenRecording={`audio/webm`} // For specific mimetype.
            />
            {rows}
        </div>
    );
}
