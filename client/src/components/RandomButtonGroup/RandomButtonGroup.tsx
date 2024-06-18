import { Alert, Box, Button } from "@mui/material";
import { baseUrl } from "../../services/api";
import { useState } from "react";

export default function RandomButtonGroup() {
  const [alerts, setAlerts] = useState({
    addVehicle: false,
    removeVehicle: false,
  });

  const addRandomVehicle = async () => {
    const res = await fetch(`${baseUrl}/api/carla/random/vehicle/add`, {
      method: "POST",
    });

    const { error, success } = await res.json();
    const alert = error || !success;

    setAlerts({ ...alerts, addVehicle: alert });
  };

  const removeRandomVehicle = async () => {
    const res = await fetch(`${baseUrl}/api/carla/random/vehicle/remove`, {
      method: "DELETE",
    });

    const { error, success } = await res.json();
    const alert = error || !success;

    setAlerts({ ...alerts, removeVehicle: alert });
  };

  return (
    <Box
      sx={{ minWidth: 100, display: "flex", flexDirection: "column", gap: 1 }}
    >
      {alerts.addVehicle && (
        <Alert severity="error">Error adding random vehicle</Alert>
      )}
      {alerts.removeVehicle && (
        <Alert severity="error">Error removing random vehicle</Alert>
      )}
        <Button variant="contained" onClick={addRandomVehicle}>Add Random Vehicle</Button>
        <Button variant="contained" onClick={removeRandomVehicle}>Remove Random Vehicles</Button>
    </Box>
  );
}
