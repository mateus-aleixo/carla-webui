import { render, screen } from "@testing-library/react";
import EgoButtonGroup from "./EgoButtonGroup";
import { useState } from "react";

test("renders EgoButtonGroup component", () => {
  const [hasEgo, setHasEgo] = useState(false);
  render(
    <EgoButtonGroup hasEgo={hasEgo} setHasEgo={(value) => setHasEgo(value)} />
  );
  expect(screen.getByText("Select Weather")).toBeInTheDocument();
});
