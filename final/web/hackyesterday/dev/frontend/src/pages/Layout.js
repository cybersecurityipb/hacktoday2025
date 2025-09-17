import { Outlet } from "react-router-dom";
import Container from 'react-bootstrap/Container';

import TopNavbar from "../components/TopNavbar";


const Layout = ({ logged, refreshLogged }) => {
  return (
    <>
        <TopNavbar logged={logged} refreshLogged={refreshLogged} />
        <Container>
          <Outlet />
        </Container>
    </>
  )
};

export default Layout;
