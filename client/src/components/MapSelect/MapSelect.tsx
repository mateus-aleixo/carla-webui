import Box from "@mui/material/Box";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select, { SelectChangeEvent } from "@mui/material/Select";
import { useState } from "react";
import { baseUrl } from "../../services/api";
import { Alert } from "@mui/material";

/**
 * MapSelect component
 * @returns MapSelect component
 * @example
 * <MapSelect />
 */
export default function MapSelect() {
  const [map, setMap] = useState("");
  const [alert, setAlert] = useState(false);

  /**
   * Fetches the selected map
   * @param map - The selected map
   * @example
   * fetchMap("Town01_Opt");
   */
  const fetchMap = async (map: string) => {
    const res = await fetch(`${baseUrl}/api/carla/map`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ map }),
    });

    const { error, success } = await res.json();

    setAlert(error || !success);
  };

  /**
   * Handles the change of the selected map
   * @param event - The event of the selected map
   * @example
   * handleChange(event);
   */
  const handleChange = (event: SelectChangeEvent) => {
    setMap(event.target.value as string);
    fetchMap(event.target.value as string);
  };

  return (
    <Box sx={{ minWidth: 100, marginBottom: 3 }}>
      {alert && (
        <Alert severity="error">Failed to set map, please try again.</Alert>
      )}
      <FormControl fullWidth>
        <InputLabel>Select Map</InputLabel>
        <Select value={map} label="map" onChange={handleChange}>
          <MenuItem value={"Town10HD_Opt"}>Default</MenuItem>
          <MenuItem value={"Town01_Opt"}>Town01</MenuItem>
          <MenuItem value={"Town02_Opt"}>Town02</MenuItem>
          <MenuItem value={"Town03_Opt"}>Town03</MenuItem>
          <MenuItem value={"Town04_Opt"}>Town04</MenuItem>
          <MenuItem value={"Town05_Opt"}>Town05</MenuItem>
        </Select>
      </FormControl>
    </Box>
  );
}
