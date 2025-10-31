import React from "react";
import { Link } from "react-router-dom";

const LandingPage = () => {
    return (
        <div className="min-h-screen flex flex-col bg-gray-950 text-white">
            {/* Hero Section */}
            <section className="flex flex-col items-center justify-center text-center py-20 px-6 flex-grow">
                <h2 className="text-5xl font-extrabold mb-6 bg-gradient-to-r from-blue-400 to-indigo-500 bg-clip-text text-transparent">
                    Smart Cheque Verification & Signature Analysis
                </h2>
                <p className="text-gray-300 max-w-2xl text-lg mb-10">
                    Chekify uses advanced AI to detect fraud, verify cheque authenticity, and compare
                    signatures with unmatched accuracy. Built for banks, fintech innovators, and researchers.
                </p>
                <div className="space-x-4">
                    <Link
                        to="/cheque-verification"
                        className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-300"
                    >
                        Try Verification
                    </Link>
                    <Link
                        to="/compare-signatures"
                        className="border border-blue-400 hover:bg-blue-400 hover:text-white font-semibold py-3 px-6 rounded-lg transition-all duration-300"
                    >
                        Compare Signatures
                    </Link>
                </div>
            </section>

            {/* Features Section */}
            <section className="bg-gray-900 py-16 px-8">
                <h3 className="text-3xl font-semibold text-center text-blue-400 mb-10">
                    Why Choose Chekify?
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-10 max-w-6xl mx-auto">
                    <div className="bg-gray-800 rounded-lg p-6 border border-gray-700 hover:border-blue-400 transition-all">
                        <h4 className="text-xl font-semibold text-blue-300 mb-3">AI-Powered OCR</h4>
                        <p className="text-gray-300">
                            Extract cheque data instantly using high-precision Optical Character Recognition
                            fine-tuned for bank documents.
                        </p>
                    </div>
                    <div className="bg-gray-800 rounded-lg p-6 border border-gray-700 hover:border-blue-400 transition-all">
                        <h4 className="text-xl font-semibold text-blue-300 mb-3">Signature Verification</h4>
                        <p className="text-gray-300">
                            Compare signatures with intelligent image similarity metrics to detect forgeries in seconds.
                        </p>
                    </div>
                    <div className="bg-gray-800 rounded-lg p-6 border border-gray-700 hover:border-blue-400 transition-all">
                        <h4 className="text-xl font-semibold text-blue-300 mb-3">Fraud Detection</h4>
                        <p className="text-gray-300">
                            Catch suspicious patterns using our deep learning fraud-check pipeline before they cause losses.
                        </p>
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="bg-gray-950 border-t border-gray-800 py-6 text-center text-gray-400 text-sm">
                <p>© {new Date().getFullYear()} Chekify — AI-driven Cheque Verification Platform</p>
            </footer>
        </div>
    );
};

export default LandingPage;
