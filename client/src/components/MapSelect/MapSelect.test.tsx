import { render, screen } from '@testing-library/react';
import MapSelect from './MapSelect';

test('renders MapSelect component', () => {
    render(<MapSelect />);
    expect(screen.getByText('Select Map')).toBeInTheDocument();
});
