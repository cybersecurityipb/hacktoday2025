import { useState, useEffect } from 'react';

import Alert from 'react-bootstrap/Alert';

import apiClient from '../utils/apiClient';
import Challenge from '../components/Challenge';

function Challenges() {
  const [challenges, setChallenges] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchChallenges();
  }, []);

  const fetchChallenges = async () => {
    setError('');

    try {
      const response = await apiClient.get('/challenges');
      setChallenges(response.data);
    } catch (error) {
      if (error.response.status === 401) {
        setError('You need to login to access this page.');
      } else {
        setError(error.response.data.detail);
      }
    }
  };

  return (
    <>
      <h1 className="my-4 text-center">Challenges</h1>
      {error && <Alert variant="danger">{error}</Alert>}

      {challenges.map(challenge => (
        <div key={challenge.id}>
          <Challenge
            id={challenge.id}
            title={challenge.title}
            description={challenge.description}
            score={challenge.score}
            draft={challenge.draft}
            attachment_filename={challenge.attachment_filename}
            alreadySolved={challenge.solved}
          />
          <br />
        </div>
      ))}
    </>
  );
}

  
export default Challenges;
