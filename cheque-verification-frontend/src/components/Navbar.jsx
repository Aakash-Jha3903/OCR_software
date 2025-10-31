import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
    return (
        <nav className="bg-gray-900 text-white px-6 py-4 shadow-md flex items-center justify-between sticky top-0 z-50 border-b border-gray-800">
            <div className="text-2xl font-semibold tracking-wide text-blue-400 hover:text-blue-300 transition-all duration-300">
                <Link to="/">Chekify</Link>
            </div>

            {/* Navigation Links */}
            <ul className="flex space-x-8 text-lg">
                <li>
                    <Link
                        to="/"
                        className="hover:text-blue-400 transition-all duration-300"
                    >
                        Home
                    </Link>
                </li>
                <li>
                    <Link
                        to="/cheque-verification"
                        className="hover:text-blue-400 transition-all duration-300"
                    >
                        Cheque Verification
                    </Link>
                </li>
                <li>
                    <Link
                        to="/compare-signatures"
                        className="hover:text-blue-400 transition-all duration-300"
                    >
                        Compare Signatures
                    </Link>
                </li>
            </ul>
        </nav>
    );
};

export default Navbar;
