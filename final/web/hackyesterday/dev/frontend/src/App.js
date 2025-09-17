import 'bootstrap/dist/css/bootstrap.min.css';

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { isLogged } from './utils/apiClient';

import Layout from './pages/Layout';
import Challenges from './pages/Challenges';
import NoPage from './pages/NoPage';
import Leaderboard from './pages/Leaderboard';
import Register from './pages/Register';
import Login from './pages/Login';
import Profile from './pages/Profile';
import CreateChallenge from './pages/CreateChallenge';


function App() {
  const [logged, setLogged] = useState(false);
  
  const refreshLogged = () => {
    setLogged(isLogged());
  }

  useEffect(() => {
    refreshLogged();
  }, []);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout logged={logged} refreshLogged={refreshLogged} />}>
          <Route index element={<Challenges />} />
          <Route path="/challenges" element={<Challenges />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
          <Route path="/create-challenge" element={<CreateChallenge />} />
          <Route path="/register" element={<Register refreshLogged={refreshLogged} />} />
          <Route path="/login" element={<Login refreshLogged={refreshLogged} />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="*" element={<NoPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
