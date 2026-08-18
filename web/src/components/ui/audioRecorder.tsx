
import ReactDOM from "react-dom/client";
import React, { useState, forwardRef, useImperativeHandle } from "react";

import { Recorder } from 'react-voice-recorder';
import 'react-voice-recorder/dist/index.css';
import { audioBufferToWebMBlob } from "./webmAudio";
import { CustomAudioPlayer } from './customAudioPlayer';

const AudioRecorderComponent = React.forwardRef((props, ref) => {
  useImperativeHandle(ref, () => ({
    createCustomAudioPlayerFromBase64
  }));

    const overallRecordedMessage = props.overallRecordedMessage;
    const onOverallRecordedMessageChange = props.onOverallRecordedMessageChange;
    const saveAudioFile = props.saveAudioFile;
    const [inputList, setInputList] = useState<{id: string, data: any, index: number}[]>([]);

    /**
     * Appends two ArrayBuffers into a new one.
     * 
     * @param {ArrayBuffer} buffer1 The first buffer.
     * @param {ArrayBuffer} buffer2 The second buffer.
     */
    function appendBuffer(buffer1, buffer2) {
        const audioCtx = new AudioContext();
        const numberOfChannels = Math.min(buffer1.numberOfChannels, buffer2.numberOfChannels );
        const tmp = audioCtx.createBuffer(numberOfChannels, (buffer1.length + buffer2.length), buffer1.sampleRate );
        for (let i=0; i<numberOfChannels; i++) {
            const channel = tmp.getChannelData(i);
            channel.set(buffer1.getChannelData(i), 0);
            channel.set(buffer2.getChannelData(i), buffer1.length);
        }
        return tmp;
    }

    function createCustomAudioPlayerFromBase64(audioInBase64) {
        const reader = new FileReader();
        
        const byteCharacters = atob(audioInBase64);
        const byteNumbers = new Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {
            byteNumbers[i] = byteCharacters.charCodeAt(i);
        }
        const byteArray = new Uint8Array(byteNumbers);
        const blob = new Blob([byteArray], {type: "audio/webm;codecs=opus"});
        reader.onload = function (evt) {
            const audioBuffer = evt.target.result;
            const url = URL.createObjectURL(blob);
            createCustomAudioPlayer(url, blob);
        }
        reader.readAsBinaryString(blob);
    }

    function createCustomAudioPlayer(url, blob) {
        const playerIdentifier = crypto.randomUUID().substring(0, 8);
        const newElement = {id: playerIdentifier, index: inputList.length, data:<CustomAudioPlayer
            url={url} keyID={inputList.length + "_" + playerIdentifier} key={playerIdentifier} blob={blob} 
            overallRecordedMessage={overallRecordedMessage}
            saveAudioFile={saveAudioFile} onOverallRecordedMessageChange={onOverallRecordedMessageChange}/>};

        setInputList(inputList => [...inputList, newElement]);
        inputList.push(newElement);
    }

    //chunks cannot be processed - for example to determine duration
    function handleAudioStop(data): void {
        createCustomAudioPlayer(data.url, data.blob);

        handleReset();
    }

    //has to be lambda otherwise called on each component rerender, not on click
    const mergeRecordedFiles = (): void =>  {
        if (inputList.length <= 1) {
            console.log("Nothing to merge. Provide at least two sound inputs!");
            return;
        }
        console.log("Merging....");
        const audioContext = new AudioContext();
        let concatenatedBuffer = null;
        let inputElement = null;
        for(let j=0; j<inputList.length; j++) {
            inputList[j].data.props.blob.arrayBuffer()
            .then((arrayBuffer) => {
                const AudioContext = window.AudioContext || window.webkitAudioContext;
                const audioCtx = new AudioContext();
                audioCtx.decodeAudioData(arrayBuffer).then((result) => {
                    if (concatenatedBuffer === null) {
                        concatenatedBuffer = result;
                    } else {
                        concatenatedBuffer = appendBuffer(concatenatedBuffer, result);
                        audioBufferToWebMBlob(audioCtx, concatenatedBuffer).then((blob) => {
                           const playerIdentifier = crypto.randomUUID().substring(0, 8);
                           const url = window.URL.createObjectURL(blob);
                            inputElement = {id: playerIdentifier, index: inputList.length, data:<CustomAudioPlayer url={url} 
                            keyID={inputList.length + "_" + playerIdentifier} key={playerIdentifier} blob={blob} 
                            overallRecordedMessage={overallRecordedMessage} saveAudioFile={saveAudioFile}
                            onOverallRecordedMessageChange={onOverallRecordedMessageChange}/>};

                            if (inputList.length > 1 && j === inputList.length - 1) {
                                setInputList(inputList => [...inputList, inputElement]);
                                inputList.push(inputElement);
                            }
                        });
                    }
                }, (e) => {console.log(e);});
           }).then((result) => {}, (e) => {console.log(e);});
        }
    }

    function handleAudioUpload(file): void {
    }

    function handleCountDown(data): void {
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
                title={"Voice line recording"}
                audioURL={state.audioDetails.url}
                showUIAudio
                handleAudioStop={data => {handleAudioStop(data)}}
                handleAudioUpload={data => handleAudioUpload(data)}
                handleCountDown={data => handleCountDown(data)}
                handleReset={() => handleReset()}
                mimeTypeToUseWhenRecording={`audio/webm`} // For specific mimetype.
            />
            {rows}
            <div>
                <button onClick={() => {mergeRecordedFiles() }}>Merge</button>
            </div>
        </div>
    );
});

export {AudioRecorderComponent};
