import { render, screen } from "@testing-library/react";
import RandomButtonGroup from "./RandomButtonGroup";

// Test to check if RandomButtonGroup component is rendered
test("renders RandomButtonGroup component", () => {
  render(<RandomButtonGroup />);
  expect(screen.getByText("Add Random Vehicle")).toBeInTheDocument();
});
