import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Alert from 'react-bootstrap/Alert';

import { apiClient, isAdmin } from '../utils/apiClient';


function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result.split(',')[1]);
    reader.onerror = (error) => reject(error);
  });
}


const CreateChallenge = () => {
  const navigate = useNavigate();
  const [error, setError] = useState('');
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [score, setScore] = useState(100);
  const [flag, setFlag] = useState('');
  const [attachmentFile, setAttachmentFile] = useState(undefined);

  const createChallengeSubmit = async (e) => {
    e.preventDefault();
    setError('');
  
    var data = {
      title: title,
      description: description,
      score: score,
      flag: flag,
      attachment_filename: "",
      attachment_content: ""
    }; 
    if (attachmentFile) {
      data.attachment_filename = attachmentFile.name;
      data.attachment_content = await fileToBase64(attachmentFile);
    }

    try {
      await apiClient.post('/challenges', data);
      navigate('/challenges');
    } catch (error) {
      setError(error.response.data.detail[0].msg);
    }
  };

  useEffect(() => {
    if (!isAdmin()) {
      setError("You must be an admin to create a challenge!");
    }
  }, []);

  return (
    <div className="container">
      <h2 className="text-center mt-4">Create a Challenge</h2>
      {error && <Alert variant="danger">{error}</Alert>}

      <Form onSubmit={createChallengeSubmit}>
        <Form.Group controlId="title" className="mt-3">
          <Form.Label>Challenge Title</Form.Label>
          <Form.Control
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Enter challenge title"
          />
        </Form.Group>

        <Form.Group controlId="description" className="mt-3">
          <Form.Label>Challenge Description</Form.Label>
          <Form.Control
            as="textarea"
            rows={7}
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Enter challenge description"
          />
        </Form.Group>

        <Form.Group controlId="score" className="mt-3">
          <Form.Label>Challenge Score</Form.Label>
          <Form.Control
            type="number"
            value={score}
            onChange={(e) => setScore(parseInt(e.target.value))}
            placeholder="Enter challenge score"
            min="1"
          />
        </Form.Group>

        <Form.Group controlId="flag" className="mt-3">
          <Form.Label>Flag</Form.Label>
          <Form.Control
            type="text"
            value={flag}
            onChange={(e) => setFlag(e.target.value)}
            placeholder="Enter the challenge flag"
          />
        </Form.Group>

        <Form.Group controlId="attachmentFile" className="mt-3">
          <Form.Label>Attachment Content</Form.Label>
          <Form.Control
            type="file"
            onChange={(e) => setAttachmentFile(e.target.files[0])}
          />
        </Form.Group>

        <Button variant="primary" type="submit" className="mt-3">
          Create Challenge
        </Button>
      </Form>
    </div>
  );
};

export default CreateChallenge;
