import 'bootstrap/dist/css/bootstrap.min.css';
import { Container, Navbar, Card } from 'react-bootstrap';
import SymptomTable from './components/SymptomTable';
import './App.css';

function App() {
  return (
    <div className="App">
      <Navbar bg="dark" variant="dark">
        <Container>
          <Navbar.Brand href="/">Health Symptoms Database</Navbar.Brand>
        </Container>
      </Navbar>
      
      <Container className="mt-4">
        <Card>
          <Card.Header>
            <h2>Health Symptoms and Recommended Products</h2>
          </Card.Header>
          <Card.Body>
            <SymptomTable />
          </Card.Body>
        </Card>
      </Container>
    </div>
  );
}

export default App;
