import { render, screen } from "@testing-library/react";
import RandomButtonGroup from "./RandomButtonGroup";

test("renders RandomButtonGroup component", () => {
  render(<RandomButtonGroup />);
  expect(screen.getByText("Select Weather")).toBeInTheDocument();
});
