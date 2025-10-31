import React, { useState } from 'react';
import axios from 'axios';

const CompareChequeSignatures = () => {
    const [file1, setFile1] = useState(null);
    const [file2, setFile2] = useState(null);
    const [responseMessage, setResponseMessage] = useState("");
    const [matchResult, setMatchResult] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

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
        setFile1(null);
        setFile2(null);
        setIsLoading(true);
        setResponseMessage("Verifying signatures, please wait...");
        setMatchResult(null);

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
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-950 text-white">
            <div className="bg-gray-900 shadow-lg rounded-lg p-8 w-full max-w-md border border-gray-800">
                <h1 className="text-3xl font-semibold text-center text-blue-400 mb-6">
                    Compare Cheque Signatures
                </h1>
                <form onSubmit={handleSubmit} className="space-y-5">
                    {/* First Cheque Upload */}
                    <div>
                        <label className="block text-gray-300 font-medium mb-2">
                            Upload First Cheque Image
                        </label>
                        <input
                            type="file"
                            onChange={handleFileChange1}
                            className="block w-full text-sm text-gray-300 file:mr-4 file:py-2 file:px-4 
                     file:rounded-lg file:border-0 file:text-sm file:font-semibold 
                     file:bg-blue-500 file:text-white hover:file:bg-blue-600 
                     cursor-pointer focus:outline-none"
                        />
                    </div>

                    {/* Second Cheque Upload */}
                    <div>
                        <label className="block text-gray-300 font-medium mb-2">
                            Upload Second Cheque Image
                        </label>
                        <input
                            type="file"
                            onChange={handleFileChange2}
                            className="block w-full text-sm text-gray-300 file:mr-4 file:py-2 file:px-4 
                     file:rounded-lg file:border-0 file:text-sm file:font-semibold 
                     file:bg-blue-500 file:text-white hover:file:bg-blue-600 
                     cursor-pointer focus:outline-none"
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={isLoading}
                        className={`w-full font-semibold py-2 px-4 rounded-lg transition-all duration-300 ${isLoading
                                ? "bg-green-600 cursor-not-allowed"
                                : "bg-blue-500 hover:bg-blue-600 text-white cursor-pointer"}`}
                    >
                        {isLoading ? "Fetching..." : "Verify Signatures"}
                    </button>
                </form>

                {/* Response Section */}
                {responseMessage && (
                    <p className="mt-5 text-center text-green-300 animate-pulse">
                        {responseMessage}
                    </p>
                )}

                {matchResult && (
                    <h3 className="mt-4 text-center text-lg font-medium text-green-400">
                        {matchResult}
                    </h3>
                )}
            </div>
        </div>
    );
};

export default CompareChequeSignatures;
