import { useState, useRef } from 'react';

interface RecordingComponentProps {
    isEmailSubmitted: boolean;
}

const RecordingComponent: React.FC<RecordingComponentProps> = ({ isEmailSubmitted }) => {
    const [isRecording, setIsRecording] = useState(false);
    const [recordingErrorMessage, setRecordingErrorMessage] = useState('');
    const [recordedVideoUrl, setRecordedVideoUrl] = useState<string | null>(null);
    const [uploadStatus, setUploadStatus] = useState<string | null>(null);
    const mediaRecorderRef = useRef<MediaRecorder | null>(null);
    const chunksRef = useRef<Blob[]>([]);

    const uploadRecording = async (blob: Blob) => {
        const formData = new FormData();
        formData.append('video', blob, 'recording1212.webm');

        try {
            setUploadStatus('Uploading...');
            const response = await fetch('http://localhost:5000/upload', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                setUploadStatus('Upload successful!');
            } else {
                setUploadStatus('Upload failed.');
            }
        } catch (error) {
            console.error('Error uploading the recording:', error);
            setUploadStatus('Upload failed.');
        }
    };

    const toggleRecording = async () => {
        if (!isEmailSubmitted) {
            setRecordingErrorMessage('Input your email before starting recording');
            return;
        }
        setRecordingErrorMessage('');

        if (isRecording) {
            if (mediaRecorderRef.current) {
                mediaRecorderRef.current.stop();
            }
            setIsRecording(false);
        } else {
            try {
                const screenStream = await navigator.mediaDevices.getDisplayMedia({
                    video: true,
                    audio: true,
                });

                const micStream = await navigator.mediaDevices.getUserMedia({
                    audio: true,
                });

                const combinedStream = new MediaStream([
                    ...screenStream.getTracks(),
                    ...micStream.getAudioTracks(),
                ]);

                const mediaRecorder = new MediaRecorder(combinedStream);
                mediaRecorderRef.current = mediaRecorder;

                mediaRecorder.ondataavailable = (event) => {
                    if (event.data.size > 0) {
                        chunksRef.current.push(event.data);
                    }
                };

                mediaRecorder.onstop = () => {
                    const blob = new Blob(chunksRef.current, { type: 'video/webm' });
                    setRecordedVideoUrl(URL.createObjectURL(blob));
                    chunksRef.current = [];
                    uploadRecording(blob); // Upload the recording
                };

                mediaRecorder.start();
                setIsRecording(true);
            } catch (error) {
                console.error('Error during recording:', error);
            }
        }
    };

    return (
        <div>
            {isRecording ? (
                <button
                    onClick={toggleRecording}
                    className="recording-button stop"
                    disabled={!isEmailSubmitted}
                >
                    Stop recording
                </button>
            ) : (
                <button
                    onClick={toggleRecording}
                    className="recording-button start"
                    disabled={!isEmailSubmitted}
                >
                    Start recording
                </button>
            )}
            {recordingErrorMessage && <p className="error-message">{recordingErrorMessage}</p>}
            {recordedVideoUrl && (
                <div style={{ marginTop: '20px' }}>
                    <h2>Recorded Video:</h2>
                    <video
                        src={recordedVideoUrl}
                        controls
                        style={{ width: '100%', maxWidth: '600px' }}
                    />
                </div>
            )}
            {uploadStatus && <p>{uploadStatus}</p>}
        </div>
    );
};

export default RecordingComponent;
