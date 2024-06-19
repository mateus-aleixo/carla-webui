import { render, screen } from "@testing-library/react";
import EgoButtonGroup from "./EgoButtonGroup";
import { useState } from "react";
import { MapInfo } from "../../types/MapInfo";

// Test to check if EgoButtonGroup component is rendered
test("renders EgoButtonGroup component", () => {
  const [hasEgo, setHasEgo] = useState(false);
  const [mapInfo, setMapInfo] = useState<MapInfo>({
    size: [] as number[],
    spawn_points: [] as number[][],
    sign_locations: [] as number[][],
    vehicle_locations: [] as number[][],
    ego_location: [] as number[],
    spectator_location: [] as number[],
  });

  render(
    <EgoButtonGroup
      hasEgo={hasEgo}
      setHasEgo={(value) => setHasEgo(value)}
      mapInfo={mapInfo}
      setMapInfo={(value) => setMapInfo(value)}
    />
  );
  expect(screen.getByText("Add EGO Vehicle")).toBeInTheDocument();
});
