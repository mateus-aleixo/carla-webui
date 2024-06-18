import { render, screen } from "@testing-library/react";
import RemoveLayers from "./RemoveLayers";

test("renders RemoveLayers component", () => {
  render(<RemoveLayers />);
  expect(screen.getByText("All")).toBeInTheDocument();
});
