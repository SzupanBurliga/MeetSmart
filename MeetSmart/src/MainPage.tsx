import { useState } from 'react';
import './App.css';

function EmailForm() {
    const [email, setEmail] = useState('');
    const [isRecording, setIsRecording] = useState(false);

    const handleSubmit = () => {
        alert(`Email submitted: ${email}`);
    };

    const handleClear = () => {
        setEmail('');
    };

    const toggleRecording = () => {
        setIsRecording(!isRecording);
    };

    return (
        <div className="email-form">
            <div className="email-input-group">
                <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Enter your email"
                />
                <button onClick={handleSubmit}>Submit</button>
            </div>
            <button
                onClick={toggleRecording}
                className={`recording-button ${isRecording ? 'stop' : 'start'}`}
            >
                {isRecording ? 'Stop recording' : 'Start recording'}
            </button>
            <button onClick={handleClear}>Start processing the meeting</button>
        </div>
    );
}

export default EmailForm;