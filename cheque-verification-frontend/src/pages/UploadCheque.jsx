import React, { useState } from 'react';
import axios from 'axios';

const UploadCheque = () => {
    const [file, setFile] = useState(null);
    const [responseMessage, setResponseMessage] = useState("");
    const [chequeData, setChequeData] = useState(null);
    const [metaData, setMetaData] = useState(null);
    const [ocrImage, setOcrImage] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file) {
            setResponseMessage("Please upload a cheque image first!");
            return;
        }
        const formData = new FormData();
        formData.append('image', file);
        setChequeData(null);
        setMetaData(null);
        setOcrImage(null);
        setIsLoading(true);
        setResponseMessage("Extracting data, please wait...");

        try {
            const response = await axios.post('http://localhost:8000/api/upload/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            console.log('Response:', response.data);

            setChequeData(response.data.fields);
            setMetaData(response.data.metadata);
            setOcrImage(response.data.ocr_image);
            setResponseMessage("Cheque uploaded and processed!");
        }
        catch (error) {
            console.error('Error uploading file:', error);
            setResponseMessage("Error uploading file");
        }
        finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-950 text-white">
            <div className="bg-gray-900 shadow-lg rounded-lg p-8 w-full max-w-md border border-gray-800">
                <h1 className="text-3xl font-semibold text-center text-blue-400 mb-6">
                    Cheque Verification
                </h1>

                {/* Upload Form */}
                <form onSubmit={handleSubmit} className="flex flex-col items-center space-y-5">
                    <input
                        type="file"
                        onChange={handleFileChange}
                        className="block w-full text-sm text-gray-300 file:mr-4 file:py-2 file:px-4 
                   file:rounded-lg file:border-0 file:text-sm file:font-semibold 
                   file:bg-blue-500 file:text-white hover:file:bg-blue-600 
                   cursor-pointer focus:outline-none"
                    />
                    <button
                        type="submit"
                        disabled={isLoading}
                        className={`w-full font-semibold py-2 px-4 rounded-lg transition-all duration-300 ${isLoading ? "bg-green-600 cursor-not-allowed" : "bg-blue-500 hover:bg-blue-600 text-white cursor-pointer"}`}
                    >
                        {isLoading ? "Fetching..." : "Upload Cheque"}
                    </button>
                </form>

                {/* Response Message */}
                {responseMessage && (
                    <p className="mt-5 text-center text-green-300 animate-pulse">
                        {responseMessage}
                    </p>
                )}

                {/* OCR Result Image */}
                {ocrImage && (
                    <div className="mt-8 text-center">
                        <h3 className="text-lg font-semibold text-blue-300 mb-3">OCR Result</h3>
                        <h3 className="text-lg font-semibold text-blue-300 mb-3 text-left">Uploaded image:</h3>
                        <img
                            src={`data:image/png;base64,${ocrImage}`}
                            alt="OCR Result"
                            className="w-full max-h-80 object-contain rounded-lg border border-gray-800 shadow-md"
                        />
                    </div>
                )}

                {/* Extracted Data Section */}
                {chequeData && (
                    <div className="max-h-80">
                        <h3 className="text-lg font-semibold text-blue-300 my-3">Extracted Data:</h3>
                        <ul className="bg-gray-800 rounded-lg p-4 space-y-2 border border-gray-700">
                            {Object.entries(chequeData).map(([key, value]) => (
                                <li key={key} className="text-gray-300 text-sm">
                                    <span className="font-semibold text-blue-400">{key}:</span> {value}
                                </li>
                            ))}
                        </ul>
                        <h3 className='text-center pt-4 font-bold text-green-400'>Confidance Average: {metaData.confidence_avg}</h3>
                    </div>
                )}
            </div>
        </div>
    );
};

export default UploadCheque;
