import { render, screen } from "@testing-library/react";
import VehiclesNumberInput from "./VehiclesNumberInput";

// Test to check if VehiclesNumberInput component is rendered
test("renders VehiclesNumberInput component", () => {
  render(<VehiclesNumberInput />);
  expect(
    screen.getByText("Update Number of Random Vehicles")
  ).toBeInTheDocument();
});
