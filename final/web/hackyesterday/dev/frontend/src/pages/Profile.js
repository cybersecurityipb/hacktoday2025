import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import Alert from 'react-bootstrap/Alert';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Badge from 'react-bootstrap/Badge';

import { removeToken } from '../utils/apiClient';
import apiClient from '../utils/apiClient';


function Profile() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isAdmin, setIsAdmin] = useState(false);
  const [lastSolve, setLastSolve] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    fetchUser();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const updateUser = async (data) => {
    setUsername(data.username);
    setPassword(data.password);
    setIsAdmin(data.is_admin);
    setLastSolve(data.last_solve);
  };

  const updateProfileSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setMessage('');

    try {
      const response = await apiClient.put("/profile/me", {
        username,
        password
      });
      updateUser(response.data);
    } catch (error) {
      setError(error.response.data.detail);
    }
  };

  const fetchUser = async () => {
    setError('');

    try {
      const response = await apiClient.get('/profile/me');
      updateUser(response.data);
    } catch (error) {
      if (error.response.status === 401) {
        removeToken();
        navigate('/login');
      }
      setError(error.response.data.detail);
    }
  };

  const checkAdmin = async () => {
    setError('');

    try {
      const response = await apiClient.get('/profile/is_admin');
      setMessage(response.data.message);
    } catch (error) {
      setError(error.response.data.detail);
    }
  }

  return (
    <div className="container">
      <h1 className="text-center mt-4">{username} profile</h1>
      <div className="text-center my-2">
        {isAdmin ? <Badge bg="success">Admin</Badge> : <Badge bg="info">User</Badge>}
      </div>
      {error && <Alert variant="danger">{error}</Alert>}
      {message && <Alert variant="success">{message}</Alert>}
      
      <div className="text-center">
        <Button className="mt-1 text-center" variant="primary" onClick={checkAdmin}>Check admin</Button>
      </div>


      <Form onSubmit={updateProfileSubmit}>
        <Form.Group controlId="username" className="mt-3">
          <Form.Label>Username</Form.Label>
          <Form.Control
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Enter a username"
          />
        </Form.Group>

        <Form.Group controlId="password" className="mt-3">
          <Form.Label>Password</Form.Label>
          <Form.Control
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter a password"
          />
        </Form.Group>

        <p className="text-center text-muted mt-4">Last solve: {lastSolve}</p>

        <Button variant="primary" type="submit" className="mt-3">
          Update profile
        </Button>
      </Form>
    </div>
  );
}

  
export default Profile;