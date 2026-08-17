import { useRef, useState, useEffect } from 'react';
import { audioBufferToWebMBlob } from "./webmAudio";
import { standardButtonColor, standardButtonHeight, secondaryButtonColor} from "@/components/styles/styles";

const LOCAL = true; 
// ── API config ────────────────────────────────────────────────────
const TO_TEXT_API = LOCAL? "http://localhost:9901" : "";


export function CustomAudioPlayer({url, keyID, blob,
                            overallRecordedMessage, onOverallRecordedMessageChange, saveAudioFile}) {
  const playerRef = useRef<any>(null);
  const [duration, setDuration] = useState(0.0);
  const [audioPlayer, setAudioPlayer] = useState({"url": url,"blob": blob});
  const [textAreaText, setTextAreaText] = useState("Text to be said by NAO. Possibly loaded from video.");

  useEffect((): string => {
    async function endTime(blob) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      const audioCtx = new AudioContext();
      const arrayBuffer = await blob.arrayBuffer();
      const result = await audioCtx.decodeAudioData(arrayBuffer);
      setDuration(result.duration);
      return result.duration.toString();
    }
    //console.log(overallRecordedMessage);
    //setTextAreaText(overallRecordedMessage[keyID]);
    endTime(blob);
  }, [blob, duration]);

  useEffect(() => {
    if (playerRef.current) {
      playerRef.current.load(); // Force browser to load new file
      playerRef.current.play().catch(err => console.log("Playback blocked:", err));
    }
  }, [audioPlayer]); // Runs every time trackUrl changes


  const handlePlay = () => {
    playerRef.current?.play();
  };

  const handlePause = () => {
    playerRef.current?.pause();
  };

  const handleStop = () => {
    playerRef.current?.stop();
  };

  const handleFocus = () => {
    playerRef.current?.focus();
  };

  const endTime = async (blob): string => {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    const audioCtx = new AudioContext();
    const arrayBuffer = await blob.arrayBuffer();
    const result = await audioCtx.decodeAudioData(arrayBuffer);
    console.log(result.duration);
    
    return result.duration.toString();
  }

  async function clipAudioBufferInWebmFormat(audioContext, audioBuffer, startSec, endSec) {
        const fullBuffer = await audioContext.decodeAudioData(audioBuffer);

        const duration = fullBuffer.duration;
        const sampleRate = fullBuffer.sampleRate;
        const numChannels = fullBuffer.numberOfChannels;

        const actualStart = Math.max(0, Math.min(startSec, duration));
        const actualEnd = Math.max(actualStart, Math.min(endSec, duration));

        const startOffset = Math.floor(actualStart * sampleRate);
        const endOffset = Math.floor(actualEnd * sampleRate);
        const frameCount = endOffset - startOffset;

        const clippedBuffer = audioContext.createBuffer(numChannels, frameCount, sampleRate);

        for (let channel = 0; channel < numChannels; channel++) {
            const originalChannelData = fullBuffer.getChannelData(channel);
            const clippedChannelData = clippedBuffer.getChannelData(channel);
            
            const slicedData = originalChannelData.subarray(startOffset, endOffset);
            clippedChannelData.set(slicedData);
        }

        return clippedBuffer;
    }

  function handleClip(event): void {
      event.preventDefault();
      const form = event.target;
      const formData = new FormData(form);
      const startInterval = formData.get("startInterval");
      const endInterval = formData.get("endInterval");

      blob.arrayBuffer()
          .then((arrayBuffer) => {
              const audioCtx = new AudioContext();
              clipAudioBufferInWebmFormat(audioCtx, arrayBuffer, startInterval, endInterval).then(
                (clippedBuffer) => {
                  console.log(clippedBuffer);
                    audioBufferToWebMBlob(audioCtx, clippedBuffer).then((blob) => {
                        const url = window.URL.createObjectURL(blob);
                        //inputElement = {id: index, data:<CustomAudioPlayer url={url} key={inputList.length + 1} keyID={inputList.length + 1} blob={blob} />};
                        
                        setAudioPlayer(url, blob);
                        audioPlayer.url = url;
                        audioPlayer.blob = blob;
                        playerRef.src = url;
                        playerRef.current.innerHTML = "<source src=\"" + url + "\" type=\"audio/webm\"/>";
                        playerRef.current?.pause();
                        playerRef.current?.load();
                        playerRef.current?.play();
                        console.log(audioPlayer.url);
                    });
                });
          });
  }

 const extractFromVideo = async () => {
      const audioBlob = audioPlayer.blob;
      const audioFile = await fetch(audioPlayer.url);
      const reader = new FileReader();
      reader.readAsDataURL(audioBlob);
      reader.onloadend = async () => {
        const audioInBase64 = reader.result.replaceAll("data:audio/*;base64,","");
        const res = await fetch(`${TO_TEXT_API}/translate/webm`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ "audio_file": audioInBase64, "language": "sk", "model": "large-v1" }),
        });
        if (!res.ok) throw new Error(`Upload failed: HTTP ${res.status}`);
        const data = await res.json();
        console.log(data);
        const translation: string = data.translation;
        setTextAreaText(translation);

        if (keyID === undefined) { keyID = 0; };
        overallRecordedMessage[keyID] = translation;

        saveAudioFile(audioInBase64, keyID + ".webm");
        overallRecordedMessage["extractedText"] = translation;
        console.log(overallRecordedMessage);
        onOverallRecordedMessageChange(overallRecordedMessage);
      };   
 }

  return (
    <div>
      <audio ref={playerRef} src={audioPlayer.url} autoPlay preload="auto" controls>
        <source src={audioPlayer.url} type="audio/webm"/>
      </audio>
      <div style={{display: "flex", flexDirection: "row", justifyItems: "center", justifyContent: "center", height: "75px"}}>
          <button style={{width: "125px", height: "50px"}} onClick={handlePlay}>Play</button>
          <button style={{width: "125px", height: "50px"}} onClick={handlePause}>Pause</button>
          <button style={{width: "125px", height: "50px"}} onClick={handleStop}>Stop</button>
          <button style={{width: "125px", height: "50px"}} onClick={handleFocus}>Focus</button>
      </div>
      <form onSubmit={handleClip}>
        <div style={{display: "flex", justifyContent: "space-between", flexDirection: "row", width: "70%", height: "75px"}}>
          <span style={{display: "flex", flexDirection: "row", border: "3px solid black", justifyItems: "center", justifyContent: "center", height: "50px"}}>
            <span style={{display: "inner-flex", alignItems: "center", position: "relative", width: "17%", height: "50px"}}>
              <input name="startInterval" step=".01" type="number" defaultValue="0.0" style={{width: "100%", height: "50px"}}/>
              <span style={{position: "absolute", top: "13px",  height: "50px", alignSelf: "center"}}>s</span>
            </span>
            <span style={{margin: "0 25px 0 25px", alignSelf: "center"}}>-</span>
            <span  style={{display: "inner-flex", alignItems: "center",  position: "relative", width: "17%", height: "50px"}}>
              <input style={{width: "100%", height: "50px"}} step=".01" name="endInterval" type="number" value={duration}
              onChange={e => setDuration(audioPlayer.blob, duration)}/>
              <span style={{position: "absolute", top: "13px", height: "50px", alignSelf: "center"}}>s</span>
            </span>
          </span>
          <span style={{flex: "1"}}></span>
          <input type="submit" value="Clip" style={{width: "175px", height: "50px", backgroundColor: secondaryButtonColor, borderRadius: "15px"}} />
        </div>
        
      </form>
      <textarea style={{width: "100%", height: "100px", border: "1px solid black", borderRadius: "25px", padding: "30px 30px 30px 30px"}} name="textFromVideo" value={textAreaText} onChange={e => {}}>
  
      </textarea>
      <button style={{width: "80%", margin: "10px 10% 10px 10%", fontWeight: "bold", color: "white", height: standardButtonHeight, backgroundColor: standardButtonColor}} onClick={extractFromVideo}>Extract text from video</button>
    </div>
  );
}