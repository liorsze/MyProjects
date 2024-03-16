import { render, screen } from '@testing-library/react';
import App from './searchMovies';
import './style.css';
test('renders learn react link', () => {
  render(<App />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});
