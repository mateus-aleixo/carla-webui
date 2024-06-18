import { baseUrl } from "../../services/api";
import { Alert, Box, Button, TextField } from "@mui/material";
import { useState } from "react";

export default function NumberInputIntroduction() {
  const [value, setValue] = useState(0);
  const [alert, setAlert] = useState(false);
  const [error, setError] = useState(false);
  const [vehicles_added, setVehiclesAdded] = useState(0);

  const updateVehicles = async () => {
    setVehiclesAdded(0);

    const res = await fetch(`${baseUrl}/api/carla/random/vehicles`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        num_vehicles: value,
      }),
    });

    const { error, success, vehicles_spawned } = await res.json();

    setError(error || !success);

    if (vehicles_spawned) {
      setVehiclesAdded(vehicles_spawned);
    }
  };

  const updateValue = (e: React.ChangeEvent<HTMLInputElement>) => {
    const v = parseInt(e.target.value);

    if (v < 0 || v > 100) {
      setAlert(true);
    } else {
      setValue(v);
      setAlert(false);
      setError(false);
    }
  };

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        gap: 2,
        alignItems: "stretch",
        marginBottom: 3,
      }}
    >
      {alert && (
        <Alert severity="error">
          Number of vehicles must be between 0 and 100
        </Alert>
      )}
      {error && (
        <Alert severity="error">
          An error occurred while adding vehicles, {vehicles_added} vehicles
          were added
        </Alert>
      )}
      <TextField
        onChange={updateValue}
        value={value}
        type="number"
        variant="outlined"
      />
      <Button variant="contained" onClick={updateVehicles}>
        Update Number of Random Vehicles
      </Button>
    </Box>
  );
}
