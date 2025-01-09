import { useState } from 'react';
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

    const toggleRecording = (startRecording: () => void, stopRecording: () => void) => {
        if (!isEmailSubmitted) {
            setRecordingErrorMessage('Input your email before starting recording');
            return;
        }
        setRecordingErrorMessage('');
        if (isRecording) {
            stopRecording();
        } else {
            startRecording();
        }
        setIsRecording(!isRecording);
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
            <ReactMediaRecorder
                screen
                audio
                render={({ status, startRecording, stopRecording, mediaBlobUrl }) => (
                    <div>
                        {status !== 'idle' && status !== 'stopped' && status !== 'recording' && <p>{status}</p>}
                        <button
                            onClick={() => toggleRecording(startRecording, stopRecording)}
                            className={`recording-button ${isRecording ? 'stop' : 'start'}`}
                            disabled={!isEmailSubmitted}
                        >
                            {isRecording ? 'Stop recording' : 'Start recording'}
                        </button>
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
                        <video src={mediaBlobUrl} controls autoPlay loop />
                    </div>
                )}
            />
        </div>
    );
}

export default EmailForm;