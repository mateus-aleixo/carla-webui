import { render, screen } from "@testing-library/react";
import MapSelect from "./MapSelect";

// Test to see if the MapSelect component renders
test("renders MapSelect component", () => {
  render(<MapSelect />);
  expect(screen.getByText("Select Map")).toBeInTheDocument();
});
