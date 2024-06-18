import { styled } from "@mui/material/styles";
import Checkbox, { CheckboxProps } from "@mui/material/Checkbox";
import { FormGroup, FormControlLabel, Box, Alert } from "@mui/material";
import { useEffect, useState } from "react";
import { baseUrl } from "../../services/api";

const BpIcon = styled("span")(({ theme }) => ({
  borderRadius: 5,
  width: 25,
  height: 25,
  boxShadow:
    theme.palette.mode === "dark"
      ? "0 0 0 1px rgb(16 22 26 / 40%)"
      : "inset 0 0 0 1px rgba(16,22,26,.2), inset 0 -1px 0 rgba(16,22,26,.1)",
  backgroundColor: theme.palette.mode === "dark" ? "#394b59" : "#f5f8fa",
  backgroundImage:
    theme.palette.mode === "dark"
      ? "linear-gradient(180deg,hsla(0,0%,100%,.05),hsla(0,0%,100%,0))"
      : "linear-gradient(180deg,hsla(0,0%,100%,.8),hsla(0,0%,100%,0))",
  ".Mui-focusVisible &": {
    outline: "2px auto rgba(19,124,189,.6)",
    outlineOffset: 2,
  },
  "input:hover ~ &": {
    backgroundColor: theme.palette.mode === "dark" ? "#30404d" : "#ebf1f5",
  },
  "input:disabled ~ &": {
    boxShadow: "none",
    background:
      theme.palette.mode === "dark"
        ? "rgba(57,75,89,.5)"
        : "rgba(206,217,224,.5)",
  },
}));

const BpCheckedIcon = styled(BpIcon)({
  backgroundColor: "#137cbd",
  backgroundImage:
    "linear-gradient(180deg,hsla(0,0%,100%,.1),hsla(0,0%,100%,0))",
  "&::before": {
    display: "block",
    width: 25,
    height: 25,
    backgroundImage:
      "url(\"data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath" +
      " fill-rule='evenodd' clip-rule='evenodd' d='M12 5c-.28 0-.53.11-.71.29L7 9.59l-2.29-2.3a1.003 " +
      "1.003 0 00-1.42 1.42l3 3c.18.18.43.29.71.29s.53-.11.71-.29l5-5A1.003 1.003 0 0012 5z' fill='%23fff'/%3E%3C/svg%3E\")",
    content: '""',
  },
  "input:hover ~ &": {
    backgroundColor: "#106ba3",
  },
});

function BpCheckbox(props: CheckboxProps) {
  return (
    <Checkbox
      sx={{
        "&:hover": { bgcolor: "transparent" },
      }}
      disableRipple
      color="default"
      checkedIcon={<BpCheckedIcon />}
      icon={<BpIcon />}
      inputProps={{ "aria-label": "Checkbox demo" }}
      {...props}
    />
  );
}

export default function RemoveLayers() {
  const [layers, setLayers] = useState({
    Buildings: false,
    Decals: false,
    Foliage: false,
    Ground: false,
    ParkedVehicles: false,
    Particles: false,
    Props: false,
    StreetLights: false,
    Walls: false,
    NONE: false,
    All: true,
  });
  const [alert, setAlert] = useState(false);

  const fetchLayer = async () => {
    const res = await fetch(`${baseUrl}/api/carla/layers`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ layers }),
    });

    const { error, success } = await res.json();

    setAlert(error || !success);
  };

  const handleChange = (layer: string) => {
    if (layer === "All") {
      setLayers({
        Buildings: false,
        Decals: false,
        Foliage: false,
        Ground: false,
        ParkedVehicles: false,
        Particles: false,
        Props: false,
        StreetLights: false,
        Walls: false,
        NONE: false,
        All: true,
      });
    } else if (layer === "NONE") {
      setLayers({
        Buildings: false,
        Decals: false,
        Foliage: false,
        Ground: false,
        ParkedVehicles: false,
        Particles: false,
        Props: false,
        StreetLights: false,
        Walls: false,
        NONE: true,
        All: false,
      });
    } else {
      setLayers({
        Buildings:
          layer === "Buildings" ? !layers["Buildings"] : layers["Buildings"],
        Decals: layer === "Decals" ? !layers["Decals"] : layers["Decals"],
        Foliage: layer === "Foliage" ? !layers["Foliage"] : layers["Foliage"],
        Ground: layer === "Ground" ? !layers["Ground"] : layers["Ground"],
        ParkedVehicles:
          layer === "ParkedVehicles"
            ? !layers["ParkedVehicles"]
            : layers["ParkedVehicles"],
        Particles:
          layer === "Particles" ? !layers["Particles"] : layers["Particles"],
        Props: layer === "Props" ? !layers["Props"] : layers["Props"],
        StreetLights:
          layer === "StreetLights"
            ? !layers["StreetLights"]
            : layers["StreetLights"],
        Walls: layer === "Walls" ? !layers["Walls"] : layers["Walls"],
        NONE: false,
        All: false,
      });
    }
  };

  useEffect(() => {
    fetchLayer();
  }, [fetchLayer, layers]);

  return (
    <Box sx={{ minWidth: 100 }}>
      {alert && (
        <Alert severity="error">
          Failed to remove layers, please try again.
        </Alert>
      )}
      <FormGroup>
        <div>
          <FormControlLabel
            onChange={() => handleChange("Buildings")}
            control={<BpCheckbox checked={layers["Buildings"]} />}
            label="Buildings"
          />
          <FormControlLabel
            onChange={() => handleChange("Decals")}
            control={<BpCheckbox checked={layers["Decals"]} />}
            label="Decals"
          />
          <FormControlLabel
            onChange={() => handleChange("Foliage")}
            control={<BpCheckbox checked={layers["Foliage"]} />}
            label="Foliage"
          />
          <FormControlLabel
            onChange={() => handleChange("Ground")}
            control={<BpCheckbox checked={layers["Ground"]} />}
            label="Ground"
          />
          <FormControlLabel
            onChange={() => handleChange("ParkedVehicles")}
            control={<BpCheckbox checked={layers["ParkedVehicles"]} />}
            label="Parked Vehicles"
          />
          <FormControlLabel
            onChange={() => handleChange("Particles")}
            control={<BpCheckbox checked={layers["Particles"]} />}
            label="Particles"
          />
          <FormControlLabel
            onChange={() => handleChange("Props")}
            control={<BpCheckbox checked={layers["Props"]} />}
            label="Props"
          />
          <FormControlLabel
            onChange={() => handleChange("StreetLights")}
            control={<BpCheckbox checked={layers["StreetLights"]} />}
            label="Street Lights"
          />
          <FormControlLabel
            onChange={() => handleChange("Walls")}
            control={<BpCheckbox checked={layers["Walls"]} />}
            label="Walls"
          />
        </div>
        <div>
          <FormControlLabel
            onChange={() => handleChange("NONE")}
            control={<BpCheckbox checked={layers["NONE"]} />}
            label="None"
          />
          <FormControlLabel
            onChange={() => handleChange("All")}
            control={<BpCheckbox checked={layers["All"]} />}
            label="All"
          />
        </div>
      </FormGroup>
    </Box>
  );
}
