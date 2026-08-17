
import ReactDOM from "react-dom/client";
import React, { useState } from "react";

import { Recorder } from 'react-voice-recorder';
import 'react-voice-recorder/dist/index.css';
import { audioBufferToWebMBlob } from "./webmAudio";
import { CustomAudioPlayer } from './customAudioPlayer';

export function AudioRecorderComponent({ overallRecordedMessage, onOverallRecordedMessageChange, mainVoiceLinesChange }) {
    /*function dictToList(overallRecordedMessage: any) {
        const array = [];
        for (let i = 0; i<Object.keys(overallRecordedMessage).length; i++) {
            array.push({"id": i, "data": overallRecordedMessage[i]});
        }
        return array;
    }*/

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
        const numberOfChannels = Math.min(buffer1.numberOfChannels, buffer2.numberOfChannels );
        const tmp = audioCtx.createBuffer(numberOfChannels, (buffer1.length + buffer2.length), buffer1.sampleRate );
        for (var i=0; i<numberOfChannels; i++) {
            const channel = tmp.getChannelData(i);
            channel.set(buffer1.getChannelData(i), 0);
            channel.set(buffer2.getChannelData(i), buffer1.length);
        }
        return tmp;
    }

    //chunks cannot be processed - for example to determine duration
    function handleAudioStop(data, index): void {
        const newElement = {id: index, data:<CustomAudioPlayer mainVoiceLinesChange={mainVoiceLinesChange}
            url={data.url} keyID={index} key={index} blob={data.blob} overallRecordedMessage={overallRecordedMessage} onOverallRecordedMessageChange={onOverallRecordedMessageChange}/>};
        console.log(data);
        console.log(index);

        setInputList(inputList => [...inputList, newElement]);
        inputList.push(newElement);

        handleReset();
    }

    //has to be lambda otherwise called on each component rerender, not on click
    const mergeRecordedFiles = (): void =>  {
        if (inputList.length <= 1) {
            console.log("Nothing to merge. Provide at least two sound inputs!");
            return;
        }
        console.log("Merging....");
        console.log(inputList.length);
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
                        //console.log(concatenatedBuffer);
                        audioBufferToWebMBlob(audioCtx, concatenatedBuffer).then((blob) => {
                           let assignedIndexIdentifier = 0;

                           if (inputList !== undefined) { assignedIndexIdentifier = inputList.length + 1; }
                          console.log(assignedIndexIdentifier);
                           const url = window.URL.createObjectURL(blob);
                            inputElement = {id: index, data:<CustomAudioPlayer url={url} keyID={assignedIndexIdentifier} key={assignedIndexIdentifier} blob={blob}
                            mainVoiceLinesChange={mainVoiceLinesChange} 
                            overallRecordedMessage={overallRecordedMessage} onOverallRecordedMessageChange={onOverallRecordedMessageChange}/>};

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
         //console.log(file);
    }

    function handleCountDown(data): void {
        //console.log(data);
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
    console.log("Redrawing");
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
            <div>
                <button onClick={mergeRecordedFiles}>Merge</button>
            </div>
        </div>
    );
}
