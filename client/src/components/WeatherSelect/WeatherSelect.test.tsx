import { render, screen } from "@testing-library/react";
import WeatherSelect from "./WeatherSelect";

// Test to check if WeatherSelect component is rendered
test("renders WeatherSelect component", () => {
  render(<WeatherSelect />);
  expect(screen.getByText("Select Weather")).toBeInTheDocument();
});
