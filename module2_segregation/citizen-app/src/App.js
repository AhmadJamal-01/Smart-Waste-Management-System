import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Home        from './pages/Home';
import Scan        from './pages/Scan';
import Result      from './pages/Result';
import Rewards     from './pages/Rewards';
import Leaderboard from './pages/Leaderboard';
import NavBar      from './components/NavBar';

export default function App() {
  return (
    <BrowserRouter>
      <Toaster position="top-center" toastOptions={{
        style: { background: '#1E293B', color: '#F1F5F9', border: '1px solid #334155' }
      }}/>
      <Routes>
        <Route path="/"            element={<Home />} />
        <Route path="/scan"        element={<Scan />} />
        <Route path="/result"      element={<Result />} />
        <Route path="/rewards"     element={<Rewards />} />
        <Route path="/leaderboard" element={<Leaderboard />} />
      </Routes>
      <NavBar />
    </BrowserRouter>
  );
}

