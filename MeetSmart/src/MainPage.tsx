import { useState, useRef } from 'react';
import { ReactMediaRecorder } from 'react-media-recorder';
import './App.css';

function EmailForm() {
    const [email, setEmail] = useState('');
    const [isRecording, setIsRecording] = useState(false);
    const [isProcessing, setIsProcessing] = useState(false);
    const [isEmailSubmitted, setIsEmailSubmitted] = useState(false);
    const [validationMessage, setValidationMessage] = useState('');
    const [successMessage, setSuccessMessage] = useState('');
    const [recordingErrorMessage, setRecordingErrorMessage] = useState('');
    const [recordedVideoUrl, setRecordedVideoUrl] = useState<string | null>(null);
    const mediaRecorderRef = useRef<MediaRecorder | null>(null);
    const chunksRef = useRef<Blob[]>([]);

    const validateEmail = (email: string) => {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    };

    const handleSubmit = () => {
        if (!validateEmail(email)) {
            setValidationMessage('Invalid email format');
            setSuccessMessage('');
            return;
        }
        setValidationMessage('');
        setSuccessMessage('Email submitted successfully');
        setIsEmailSubmitted(true);
    };

    const handleClear = () => {
        setEmail('');
        setIsEmailSubmitted(false);
    };

    const toggleRecording = async () => {
        if (!isEmailSubmitted) {
            setRecordingErrorMessage('Input your email before starting recording');
            return;
        }
        setRecordingErrorMessage('');

        if (isRecording) {
            // Zatrzymaj nagrywanie
            if (mediaRecorderRef.current) {
                mediaRecorderRef.current.stop();
            }
            setIsRecording(false);
        } else {
            try {
                // Pobierz ekran i audio (jeśli dostępne)
                const screenStream = await navigator.mediaDevices.getDisplayMedia({
                    video: true,
                    audio: true, // Próbujemy przechwycić dźwięk systemowy
                });

                // Pobierz mikrofon jako zapasowe źródło audio
                const micStream = await navigator.mediaDevices.getUserMedia({
                    audio: true,
                });

                // Połącz strumień ekranu i mikrofonu
                const combinedStream = new MediaStream([
                    ...screenStream.getTracks(),
                    ...micStream.getAudioTracks(),
                ]);

                // Sprawdź, jakie ścieżki są dostępne
                combinedStream.getTracks().forEach((track) => {
                    console.log(`Ścieżka: ${track.kind}, label: ${track.label}`);
                });

                // Tworzymy MediaRecorder dla połączonego strumienia
                const mediaRecorder = new MediaRecorder(combinedStream);
                mediaRecorderRef.current = mediaRecorder;

                // Zapisujemy dane w trakcie nagrywania
                mediaRecorder.ondataavailable = (event) => {
                    if (event.data.size > 0) {
                        chunksRef.current.push(event.data);
                    }
                };

                // Po zakończeniu nagrywania tworzymy URL z pliku
                mediaRecorder.onstop = () => {
                    const blob = new Blob(chunksRef.current, { type: "video/webm" });
                    setRecordedVideoUrl(URL.createObjectURL(blob));
                    chunksRef.current = [];
                };

                // Rozpoczynamy nagrywanie
                mediaRecorder.start();
                setIsRecording(true);
            } catch (error) {
                console.error("Błąd podczas nagrywania:", error);
            }
        }
    };

    const processMeeting = () => {
        setIsProcessing(true);
        // Simulate processing delay
        setTimeout(() => {
            setIsProcessing(false);
        }, 2000);
    };

    return (
        <div className="email-form">
            <h1>Notes from a meeting</h1>
            <div>
                {isRecording ? (
                    <button
                        onClick={toggleRecording}
                        className={`recording-button stop`}
                        disabled={!isEmailSubmitted}
                    >
                        Stop recording
                    </button>
                ) : (
                    <button
                        onClick={toggleRecording}
                        className={`recording-button start`}
                        disabled={!isEmailSubmitted}
                    >
                        Start recording
                    </button>
                )}
                {recordingErrorMessage && <p className="error-message">{recordingErrorMessage}</p>}
                <button
                    onClick={processMeeting}
                    disabled={isProcessing}
                >
                    {isProcessing ? 'Processing...' : 'Start processing the meeting'}
                </button>
                <div className="email-input-group">
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Enter your email"
                    />
                    <button onClick={handleSubmit}>
                        {isEmailSubmitted ? 'Edit' : 'Submit'}
                    </button>
                </div>
                {validationMessage && <p className="validation-message">{validationMessage}</p>}
                {successMessage && <p className="success-message">{successMessage}</p>}
                {recordedVideoUrl && (
                    <div style={{ marginTop: "20px" }}>
                        <h2>Recorded Video:</h2>
                        <video
                            src={recordedVideoUrl}
                            controls
                            style={{ width: "100%", maxWidth: "600px" }}
                        />
                        <a
                            href={recordedVideoUrl}
                            download="meeting_recording.webm"
                            style={{
                                display: "block",
                                marginTop: "10px",
                                color: "blue",
                                textDecoration: "underline",
                            }}
                        >
                            Download Recording
                        </a>
                    </div>
                )}
            </div>
        </div>
    );
}

export default EmailForm;
