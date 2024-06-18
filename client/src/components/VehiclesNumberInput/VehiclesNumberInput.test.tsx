import { render, screen } from "@testing-library/react";
import VehiclesNumberInput from "./VehiclesNumberInput";

test("renders VehiclesNumberInput component", () => {
  render(<VehiclesNumberInput />);
  expect(screen.getByText("Select Weather")).toBeInTheDocument();
});
