import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';  // Optional: for custom navbar styles

const Navbar = () => {
    return (
        <nav className="navbar">
            <ul>
                <li><Link to="/">Home</Link></li>
                <li><Link to="/cheque-verification">Cheque Verification</Link></li>
                <li><Link to="/compare-signatures">Compare Signatures</Link></li>
            </ul>
        </nav>
    );
};

export default Navbar;
