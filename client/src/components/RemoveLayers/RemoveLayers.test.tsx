import { render, screen } from "@testing-library/react";
import RemoveLayers from "./RemoveLayers";

// Test to check if RemoveLayers component is rendered
test("renders RemoveLayers component", () => {
  render(<RemoveLayers />);
  expect(screen.getByText("All")).toBeInTheDocument();
});
