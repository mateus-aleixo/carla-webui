import { render, screen } from '@testing-library/react';
import WeatherSelect from './WeatherSelect';

test('renders WeatherSelect component', () => {
    render(<WeatherSelect />);
    expect(screen.getByText('Select Weather')).toBeInTheDocument();
});
