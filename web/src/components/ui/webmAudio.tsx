
async function audioBufferToWebMBlob(audioContext: AudioContext, audioBuffer: AudioBuffer) {
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

export { audioBufferToWebMBlob }