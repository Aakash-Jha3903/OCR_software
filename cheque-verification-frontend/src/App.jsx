import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'; // Change to Routes
import Navbar from '../src/components/Navbar';
import UploadCheque from '../src/components/UploadCheque';  // Ensure to import your existing component
import CompareChequeSignatures from '../src/components/CompareChequeSignatures';  // Ensure to import your existing component

const App = () => {
    return (
        <Router>
            <Navbar />
            <div className="container">
                <Routes> {/* Replace Switch with Routes */}
                    <Route exact path="/" element={<h2>Welcome to the Cheque Verification App</h2>} />
                    <Route path="/cheque-verification" element={<UploadCheque />} />
                    <Route path="/compare-signatures" element={<CompareChequeSignatures />} />
                </Routes>
            </div>
        </Router>
    );
};

export default App;
