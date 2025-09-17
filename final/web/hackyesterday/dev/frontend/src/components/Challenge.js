import { useState, useRef, useEffect } from 'react';

import Card from 'react-bootstrap/Card';
import InputGroup from 'react-bootstrap/InputGroup';
import Form from 'react-bootstrap/Form';
import Alert from 'react-bootstrap/Alert';

import apiClient from '../utils/apiClient';


function Challenge({id, title, description, score, draft, attachment_filename, alreadySolved}) {
    const [flag, setFlag] = useState('');
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');
    const [solved, setSolved] = useState(alreadySolved);
    const descriptionRef = useRef();

    useEffect(() => {
      descriptionRef.current.innerHTML = description;
      loadScriptDynamically();
    }, [description]);

    const loadScriptDynamically = () => {
        const scriptElements = descriptionRef.current.querySelectorAll('script');
        scriptElements.forEach((scriptElem) => {
          const newScriptElem = document.createElement('script');
          if (scriptElem.src) {
            newScriptElem.src = scriptElem.src;
          } else {
            newScriptElem.textContent = scriptElem.textContent;
          }
          descriptionRef.current.appendChild(newScriptElem);
          scriptElem.remove();
        });
    }

    const handleChangeFlag = (e) => {
        setFlag(e.target.value);
    };
  
    const handleSubmit = async (e) => {
      e.preventDefault();
      setError('');
      setMessage('');
  
      if (solved) return;

      try {
        await apiClient.post(`/challenges/${id}/solve`, { flag });
        setMessage('Congrats! You solved the challenge.');
        setFlag('');
        setSolved(true);
      } catch (error) {
        setError(error.response.data.detail);
      }
    };

    return (
        <Card>
         <Card.Header>{title}</Card.Header>
         <Card.Body>
           <blockquote className="blockquote mb-0">
             {error && <Alert variant="danger">{error}</Alert>}
             {draft && <Alert variant="warning">This challenge is a draft.</Alert>}
             <p ref={descriptionRef}></p>

             <InputGroup className="mb-3">
                <InputGroup.Text>Answer</InputGroup.Text>
                <Form.Control disabled={solved || draft} aria-label="Answer of the challenge" value={flag} onChange={handleChangeFlag} />
                <InputGroup.Text className="bg-primary text-white btn" onClick={handleSubmit}>Submit</InputGroup.Text>
             </InputGroup>

             {attachment_filename && 
              <>
                <p>Attachment: <a href={attachment_filename} target="_blank" rel="noreferrer">{attachment_filename.split("/").pop()}</a></p>
              </>
             }

             {message && <Alert variant="success">{message}</Alert>}

             <p className="text-muted text-sm">
                <small>Score {score} for challenge n°{id}.</small>
             </p>
           </blockquote>
         </Card.Body>
       </Card>
    );
}

export default Challenge;