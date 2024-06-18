import Box from "@mui/material/Box";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select, { SelectChangeEvent } from "@mui/material/Select";
import { useState } from "react";
import { baseUrl } from "../../services/api";
import { Alert } from "@mui/material";

export default function WeatherSelect() {
  const [weather, setWeather] = useState("");
  const [alert, setAlert] = useState(false);

  const fetchWeather = async (weather: string) => {
    const res = await fetch(`${baseUrl}/api/carla/weather`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ weather }),
    });

    const { error, success } = await res.json();

    setAlert(error || !success);
  };

  const handleChange = (event: SelectChangeEvent) => {
    setWeather(event.target.value as string);
    fetchWeather(event.target.value as string);
  };

  return (
    <Box sx={{ minWidth: 100, marginTop: 3, marginBottom: 3 }}>
      {alert && (
        <Alert severity="error">Failed to set weather, please try again.</Alert>
      )}
      <FormControl fullWidth>
        <InputLabel>Select Weather</InputLabel>
        <Select value={weather} label="weather" onChange={handleChange}>
          <MenuItem value={"Default"}>Default</MenuItem>
          <MenuItem value={"ClearNoon"}>Clear Noon</MenuItem>
          <MenuItem value={"CloudyNoon"}>Cloudy Noon</MenuItem>
          <MenuItem value={"WetNoon"}>Wet Noon</MenuItem>
          <MenuItem value={"WetCloudyNoon"}>Wet Cloudy Noon</MenuItem>
          <MenuItem value={"MidRainyNoon"}>Mid Rainy Noon</MenuItem>
          <MenuItem value={"HardRainNoon"}>Hard Rain Noon</MenuItem>
          <MenuItem value={"SoftRainNoon"}>Soft Rain Noon</MenuItem>
          <MenuItem value={"ClearSunset"}>Clear Sunset</MenuItem>
          <MenuItem value={"CloudySunset"}>Cloudy Sunset</MenuItem>
          <MenuItem value={"WetSunset"}>Wet Sunset</MenuItem>
          <MenuItem value={"WetCloudySunset"}>Wet Cloudy Sunset</MenuItem>
          <MenuItem value={"MidRainSunset"}>Mid Rain Sunset</MenuItem>
          <MenuItem value={"HardRainSunset"}>Hard Rain Sunset</MenuItem>
          <MenuItem value={"SoftRainSunset"}>Soft Rain Sunset</MenuItem>
        </Select>
      </FormControl>
    </Box>
  );
}
