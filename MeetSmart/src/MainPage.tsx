import { useState } from 'react';
import './App.css';
import RecordingComponent from './RecordingComponent';

function EmailForm() {
    const [email, setEmail] = useState('');
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
        setIsEmailSubmitted(true);
    };

    const handleClear = () => {
        setEmail('');
        setIsEmailSubmitted(false);
    };

    return (
        <div className="email-form">
            <h1>Notes from a meeting</h1>
            <div>
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
                <RecordingComponent isEmailSubmitted={isEmailSubmitted} />
            </div>
        </div>
    );
}

export default EmailForm;
