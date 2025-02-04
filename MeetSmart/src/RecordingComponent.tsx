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
        formData.append('video', blob, 'recording.webm');

        try {
            setUploadStatus('Wysyłanie...');
            const response = await fetch('http://localhost:5000/upload', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                setUploadStatus('Wysyłanie zakończone pomyślnie');
            } else {
                setUploadStatus('Wysyłanie nie powiodło się');
            }
        } catch (error) {
            console.error('Error uploading the recording:', error);
            setUploadStatus('Wysyłanie nie powiodło się.');
        }
    };

    const toggleRecording = async () => {
        if (!isEmailSubmitted) {
            setRecordingErrorMessage('Wprowadź email przed uruchomieniem nagrywania');
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
                    uploadRecording(blob);
                };

                mediaRecorder.start();
                setIsRecording(true);
            } catch (error) {
                console.error('Błąd podczas nagrywania:', error);
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
                    Zatrzymaj nagrywanie
                </button>
            ) : (
                <button
                    onClick={toggleRecording}
                    className="recording-button start"
                    disabled={!isEmailSubmitted}
                >
                    Rozpocznij nagrywanie
                </button>
            )}
            {recordingErrorMessage && <p className="error-message">{recordingErrorMessage}</p>}
            {recordedVideoUrl && (
                <div style={{ marginTop: '20px' }}>
                    <h2 className="success-message">Pomyślnie nagrano video</h2>
                </div>
            )}
        </div>
    );
};

export default RecordingComponent;
