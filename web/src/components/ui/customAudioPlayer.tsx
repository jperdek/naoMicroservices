import { useRef } from 'react';
import { AudioPlayer } from 'react-audio-play';

export function CustomAudioPlayer(props) {
  const playerRef = useRef<any>(null);

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
console.log(props);
  return (
    <div>
      <AudioPlayer ref={playerRef} src={props.url} autoPlay />
      <button onClick={handlePlay}>Play</button>
      <button onClick={handlePause}>Pause</button>
      <button onClick={handleStop}>Stop</button>
      <button onClick={handleFocus}>Focus</button>
    </div>
  );
}