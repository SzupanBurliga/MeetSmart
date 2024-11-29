import { useState } from 'react';
import './App.css';

function EmailForm() {
    const [email, setEmail] = useState('');
    const [isRecording, setIsRecording] = useState(false);
    const [isProcessing, setIsProcessing] = useState(false);
    const [isEmailSubmitted, setIsEmailSubmitted] = useState(false);
    const [validationMessage, setValidationMessage] = useState('');
    const [successMessage, setSuccessMessage] = useState('');

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
        if (isEmailSubmitted) {
            setIsEmailSubmitted(false);
        } else {
            setIsEmailSubmitted(true);
        }
    };

    const handleClear = () => {
        setEmail('');
    };

    const toggleRecording = () => {
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
            <button
                onClick={toggleRecording}
                className={`recording-button ${isRecording ? 'stop' : 'start'}`}
            >
                {isRecording ? 'Stop recording' : 'Start recording'}
            </button>
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
        </div>
    );
}

export default EmailForm;