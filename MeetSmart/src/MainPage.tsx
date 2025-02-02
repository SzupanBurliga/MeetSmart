import { useState, useEffect} from 'react';
import './App.css';
import RecordingComponent from './RecordingComponent';

function EmailForm() {
    const [email, setEmail] = useState('');
    const [isEmailSubmitted, setIsEmailSubmitted] = useState(false);
    const [validationMessage, setValidationMessage] = useState('');
    const [successMessage, setSuccessMessage] = useState('');

    useEffect(() => {
        if (successMessage) {
            const timer = setTimeout(() => {
                setSuccessMessage('');
            }, 3000);
            return () => clearTimeout(timer);
        }
    }, [successMessage]);

    const validateEmail = (email: string) => {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    };

    const sendEmailToServer = async (email: string) => {
        try {
            const response = await fetch('http://localhost:5000/submit-email', {
                method: 'POST',
                headers: { 'Content-Type': 'text/plain' },
                body: email,
            });

            if (response.ok) {
                console.log('Email submitted to the server successfully');
                return true;
            } else {
                console.error('Failed to submit email to the server');
                return false;
            }
        } catch (error) {
            console.error('Error submitting email to the server:', error);
            return false;
        }
    };

    const handleSubmit = async () => {
        if (!validateEmail(email)) {
            setValidationMessage('Invalid email format');
            setSuccessMessage('');
            return;
        }

        const isEmailSent = await sendEmailToServer(email);

        if (isEmailSent) {
            setValidationMessage('');
            setSuccessMessage('Email submitted successfully');
            setIsEmailSubmitted(true);
        } else {
            setValidationMessage('Failed to submit email. Please try again.');
            setSuccessMessage('');
        }
    };

    const handleClear = () => {
        setEmail('');
        setIsEmailSubmitted(false);
        setValidationMessage('');
        setSuccessMessage('');
    };

    return (
        <div className="email-form">
            <h1 className="title">Notes from a meeting</h1>
            <div>
                <div className="email-input-group">
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Enter your email"
                        disabled={isEmailSubmitted}
                    />
                    <button onClick={isEmailSubmitted ? handleClear : handleSubmit}>
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
