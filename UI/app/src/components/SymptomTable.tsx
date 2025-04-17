import React, { useEffect, useState } from 'react';
import { Table, Spinner, Alert, Badge } from 'react-bootstrap';
import { fetchSymptoms, Symptom } from '../api';

const SymptomTable: React.FC = () => {
  const [symptoms, setSymptoms] = useState<Symptom[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadSymptoms = async () => {
      try {
        const data = await fetchSymptoms();
        setSymptoms(data.results); // Extract results from paginated response
        setLoading(false);
      } catch (err) {
        setError('Failed to load symptoms from database');
        setLoading(false);
        console.error('Error loading symptoms:', err);
      }
    };

    loadSymptoms();
  }, []);

  if (loading) return <div className="text-center mt-5"><Spinner animation="border" /></div>;
  if (error) return <Alert variant="danger">{error}</Alert>;
  if (symptoms.length === 0) return <Alert variant="info">No symptoms found in the database</Alert>;

  return (
    <Table striped bordered hover responsive>
      <thead>
        <tr>
          <th>Name</th>
          <th>Applicable To</th>
          <th>Products</th>
          <th>Comments</th>
        </tr>
      </thead>
      <tbody>
        {symptoms.map(symptom => (
          <tr key={symptom.id}>
            <td>{symptom.name}</td>
            <td>
              {symptom.adult && <Badge bg="primary" className="me-1">Adult</Badge>}
              {symptom.child && <Badge bg="info">Child</Badge>}
            </td>
            <td>
              {Array.isArray(symptom.products) ? 
                symptom.products.map((productId: number) => (
                  <Badge key={productId} bg="secondary" className="me-1">Product {productId}</Badge>
                ))
                : <span>No products</span>
              }
            </td>
            <td>
              {symptom.comments && (
                <ul className="list-unstyled mb-0">
                  {Object.entries(symptom.comments).map(([key, value]) => (
                    <li key={key}><strong>{key}:</strong> {value}</li>
                  ))}
                </ul>
              )}
            </td>
          </tr>
        ))}
      </tbody>
    </Table>
  );
};

export default SymptomTable;
