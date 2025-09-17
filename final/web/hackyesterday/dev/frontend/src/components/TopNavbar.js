import { useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';

import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';

import { removeToken } from '../utils/apiClient';


function TopNavbar({ logged, refreshLogged }) {
  const navigate = useNavigate();

  function logout() {
    removeToken();
    refreshLogged();
    navigate('/');
  }

  useEffect(() => {
    refreshLogged();
  }, [refreshLogged]);

  return (
    <Navbar collapseOnSelect expand="lg" className="bg-body-tertiary">
      <Container>
        <Navbar.Brand as={Link} to="/">HackYesterday</Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link as={Link} to="/challenges">
              Challenges
            </Nav.Link>
            <Nav.Link as={Link} to="/leaderboard">
              Leaderboard
            </Nav.Link>
            <Nav.Link as={Link} to="/create-challenge">
              Create a Challenge
            </Nav.Link>
          </Nav>
          <Nav>
            {!logged && (
              <>
                <Nav.Link as={Link} to="/register">
                  Register
                </Nav.Link>
                <Nav.Link as={Link} to="/login">
                  Login
                </Nav.Link>
              </>
            )}
            {logged && (
              <>
                <Nav.Link as={Link} to="/profile">
                  Profile
                </Nav.Link>
                <Nav.Link onClick={logout}>
                  Logout
                </Nav.Link>
              </>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default TopNavbar;