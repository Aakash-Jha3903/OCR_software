import React, { useState } from 'react';
import axios from 'axios';

const UploadCheque = () => {
    const [file, setFile] = useState(null);
    const [responseMessage, setResponseMessage] = useState("");
    const [chequeData, setChequeData] = useState(null);
    const [ocrImage, setOcrImage] = useState(null);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('image', file);

        try {
            const response = await axios.post('http://localhost:8000/api/upload/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            setChequeData(response.data.cheque_data);
            setOcrImage(response.data.ocr_image);
            setResponseMessage("Cheque uploaded and processed!");
        } catch (error) {
            console.error('Error uploading file:', error);
            setResponseMessage("Error uploading file");
        }
    };

    return (
        <div>
            <h1>Cheque Verification</h1>
            <form onSubmit={handleSubmit}>
                <input type="file" onChange={handleFileChange} />
                <button type="submit">Upload Cheque</button>
            </form>
            {responseMessage && <p>{responseMessage}</p>}

            {ocrImage && (
                <div>
                    <h3>OCR Result:</h3>
                    <img src={`data:image/png;base64,${ocrImage}`} alt="OCR Result" />
                </div>
            )}

            {chequeData && (
                <div>
                    <h3>Extracted Data:</h3>
                    <ul>
                        {Object.entries(chequeData).map(([key, value]) => (
                            <li key={key}><strong>{key}:</strong> {value}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default UploadCheque;
