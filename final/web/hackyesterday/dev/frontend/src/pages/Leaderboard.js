import { useState, useEffect } from 'react';

import Table from 'react-bootstrap/Table';
import Alert from 'react-bootstrap/Alert';
import Button from 'react-bootstrap/esm/Button';

import apiClient from '../utils/apiClient';


function Leaderboard() {
  const [players, setPlayers] = useState([]);
  const [prizes, setPrizes] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    fetchPlayers();
  }, []);

  const fetchPlayers = async () => {
    setError('');

    try {
      const response = await apiClient.get('/leaderboard');
      setPlayers(response.data);
    } catch (error) {
      setError(error.response.data.detail);
    }
  };

  const fetchPrizes = async () => {
    setError('');

    try {
      const response = await apiClient.get('/prizes');
      setPrizes(response.data.message);
    } catch (error) {
      setError(error.response.data.detail);
    }
  };

  return (
    <>
      <div className="text-center my-4">
        <h1 className="my-2">Leaderboard</h1>

        <Button className="my-2" variant="primary" onClick={fetchPrizes}>Claim prizes</Button>
      </div>

      {error && <Alert variant="danger">{error}</Alert>}
      {prizes && <Alert variant="success">{prizes}</Alert>}

      <Table striped bordered hover className='my-4'>
        <thead>
          <tr>
            <th>Rank</th>
            <th>Username</th>
            <th>Score</th>
            <th>Last solve</th>
          </tr>
        </thead>
        <tbody>
          {players.map((player, index) => (
            <tr key={index}>
              <td>{index + 1}</td>
              <td>{player.username}</td>
              <td>{player.score}</td>
              <td>{player.last_solve}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </>
  );
}

export default Leaderboard;