import React, { useState } from 'react';
import axios from 'axios';

const CompareChequeSignatures = () => {
    const [file1, setFile1] = useState(null);
    const [file2, setFile2] = useState(null);
    const [responseMessage, setResponseMessage] = useState("");
    const [matchResult, setMatchResult] = useState(null);

    const handleFileChange1 = (e) => {
        setFile1(e.target.files[0]);
    };

    const handleFileChange2 = (e) => {
        setFile2(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file1 || !file2) {
            setResponseMessage("Please upload both cheque images.");
            return;
        }

        const formData = new FormData();
        formData.append('image1', file1);
        formData.append('image2', file2);

        try {
            const response = await axios.post('http://localhost:8000/api/verify_signatures/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            const { matched, match_percent } = response.data;
            if (matched) {
                setMatchResult(`✅ Signatures Match! Similarity: ${match_percent.toFixed(2)}%`);
            } else {
                setMatchResult(`❌ Signatures Do Not Match. Similarity: ${match_percent.toFixed(2)}%`);
            }
            setResponseMessage("Signature verification complete.");
        } catch (error) {
            console.error('Error uploading files:', error);
            setResponseMessage("Error verifying signatures.");
        }
    };

    return (
        <div>
            <h1>Compare Cheque Signatures</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Upload First Cheque Image:</label>
                    <input type="file" onChange={handleFileChange1} />
                </div>
                <div>
                    <label>Upload Second Cheque Image:</label>
                    <input type="file" onChange={handleFileChange2} />
                </div>
                <button type="submit">Verify Signatures</button>
            </form>
            {responseMessage && <p>{responseMessage}</p>}
            {matchResult && <h3>{matchResult}</h3>}
        </div>
    );
};

export default CompareChequeSignatures;
