import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Alert from 'react-bootstrap/Alert';

import { apiClient, setToken } from '../utils/apiClient';


function Login({ refreshLogged }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleUsernameChange = (e) => {
    setUsername(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const loginSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const response = await apiClient.post('/login', {
        username, password
      });
      setToken(response.data.access_token);
      refreshLogged();
      navigate('/challenges');
    } catch (error) {
      setError(error.response.data.detail);
    }
  };

  useEffect(() => {
    refreshLogged();
  }, [refreshLogged]);

  return (
    <div className="container">
      <h2 className="text-center mt-4">Login</h2>
      {error && <Alert variant="danger">{error}</Alert>}

      <Form onSubmit={loginSubmit}>
        <Form.Group controlId="username">
          <Form.Label>Username:</Form.Label>
          <Form.Control type="text" value={username} onChange={handleUsernameChange} />
        </Form.Group>
        <Form.Group controlId="password">
          <Form.Label>Password:</Form.Label>
          <Form.Control type="password" value={password} onChange={handlePasswordChange} />
        </Form.Group>
        <Button id="submit" variant="primary" type="submit" className="mt-3">Login</Button>
      </Form>
    </div>
  );
}

export default Login;
