import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from '../src/components/Navbar';
import Home from './pages/Home';
import UploadCheque from './pages/UploadCheque';
import CompareChequeSignatures from './pages/CompareChequeSignatures';

const App = () => {
    return (
        <Router>
            <div className="container">
                <Routes>
                    <Route exact path="/" element={<><Navbar /><Home/></>} />
                    <Route path="/cheque-verification" element={<><Navbar /><UploadCheque /></>} />
                    <Route path="/compare-signatures" element={<><Navbar /><CompareChequeSignatures /></>} />
                </Routes>
            </div>
        </Router>
    );
};

export default App;
