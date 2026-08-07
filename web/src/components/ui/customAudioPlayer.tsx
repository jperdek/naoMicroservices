import { useRef, useState, useEffect } from 'react';
import { audioBufferToWebMBlob } from "./webmAudio";

export function CustomAudioPlayer(props) {
  const playerRef = useRef<any>(null);
  const [duration, setDuration] = useState(0.0);
  const [audioPlayer, setAudioPlayer] = useState({"url": props.url,"blob": props.blob});

  useEffect((): string => {
    async function endTime(blob) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      const audioCtx = new AudioContext();
      const arrayBuffer = await blob.arrayBuffer();
      const result = await audioCtx.decodeAudioData(arrayBuffer);
      console.log(result.duration);
      setDuration(result.duration);
      return result.duration.toString();
    }
    endTime(props.blob);
  }, [props.blob, duration]);

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

      props.blob.arrayBuffer()
          .then((arrayBuffer) => {
              const audioCtx = new AudioContext();
              clipAudioBufferInWebmFormat(audioCtx, arrayBuffer, startInterval, endInterval).then(
                (clippedBuffer) => {
                  console.log(clippedBuffer);
                    audioBufferToWebMBlob(audioCtx, clippedBuffer).then((blob) => {
                        const url = window.URL.createObjectURL(blob);
                        //inputElement = {id: index, data:<CustomAudioPlayer url={url} key={inputList.length + 1} blob={blob} />};
                        
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

  console.log(props);
 
  return (
    <div>
      <audio ref={playerRef} src={audioPlayer.url} autoPlay preload="auto" controls>
        <source src={audioPlayer.url} type="audio/webm"/>
      </audio>
      <button onClick={handlePlay}>Play</button>
      <button onClick={handlePause}>Pause</button>
      <button onClick={handleStop}>Stop</button>
      <button onClick={handleFocus}>Focus</button>
      <form onSubmit={handleClip}>
        <div>
          <input name="startInterval" step=".01" type="number" defaultValue="0.0" />-<input step=".01" name="endInterval" type="number" value={duration}
          onChange={e => setDuration(audioPlayer.blob, duration)}/>
        </div>
        <input type="submit" value="Clip" />
      </form>
    </div>
  );
}