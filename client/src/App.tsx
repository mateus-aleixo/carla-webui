import { useEffect, useRef, useState } from "react";
import "./App.css";
import { baseUrl } from "./services/api";
import WeatherSelect from "./components/WeatherSelect/WeatherSelect";
import MapSelect from "./components/MapSelect/MapSelect";
import RemoveLayers from "./components/RemoveLayers/RemoveLayers";
import EgoButtonGroup from "./components/EgoButtonGroup/EgoButtonGroup";
import RandomButtonGroup from "./components/RandomButtonGroup/RandomButtonGroup";
import { Alert, Button } from "@mui/material";
import Chart from "chart.js/auto";
import VehiclesNumberInput from "./components/VehiclesNumberInput/VehiclesNumberInput";

interface WorldInfo {
  map: string;
  precipitation: number;
  wind_intensity: number;
  num_vehicles: number;
}

interface MapInfo {
  size: number[];
  spawn_points: number[][];
  actor_locations: number[][];
}

interface Sensors {
  gnss_data: { [key: string]: number };
  image: string;
}

function App() {
  const [mapInfo, setMapInfo] = useState<MapInfo>({
    size: [] as number[],
    spawn_points: [] as number[][],
    actor_locations: [] as number[][],
  });
  const [chart, setChart] = useState<Chart | null>(null);
  const [alert, setAlert] = useState(false);
  const [worldInfo, setWorldInfo] = useState<WorldInfo>({
    map: "Town10",
    precipitation: 0,
    wind_intensity: 0,
    num_vehicles: 0,
  });
  const [sensors, setSensors] = useState<Sensors>({
    gnss_data: {},
    image: "",
  });
  const [hasEgo, setHasEgo] = useState(false);
  const [loadingInfo, setLoadingInfo] = useState(false);

  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  const fetchWorldInfo = async () => {
    const res = await fetch(`${baseUrl}/api/carla/world_info`, {
      method: "GET",
    });
    const { map, precipitation, wind_intensity, num_vehicles } =
      await res.json();
    setWorldInfo({
      map: map.slice(0, 6),
      precipitation,
      wind_intensity,
      num_vehicles,
    });
  };

  const fetchVehicleLocations = async () => {
    const res = await fetch(`${baseUrl}/api/carla/vehicles`, {
      method: "GET",
    });
    const { actor_locations } = await res.json();
    setMapInfo((prev) => ({ ...prev, actor_locations }));
  };

  const fetchMapInfo = async () => {
    const res = await fetch(`${baseUrl}/api/carla/map_info`, {
      method: "GET",
    });
    const { size, spawn_points } = await res.json();
    setMapInfo((prev) => ({ ...prev, size, spawn_points }));
  };

  const fetchSensors = async () => {
    const res = await fetch(`${baseUrl}/api/carla/ego/sensors`, {
      method: "GET",
    });

    const { error, gnss_data, image } = await res.json();

    if (error) {
      setHasEgo(false);
    } else {
      setHasEgo(true);
    }

    setSensors({
      gnss_data,
      image,
    });
  };

  const removeAllActors = async () => {
    const res = await fetch(`${baseUrl}/api/carla/destroy/all`, {
      method: "DELETE",
    });
    const { error, success } = await res.json();
    setAlert(error || !success);
  };

  const checkIfEgoExists = async () => {
    const res = await fetch(`${baseUrl}/api/carla/ego/vehicle`, {
      method: "GET",
    });
    const { has_ego } = await res.json();
    setHasEgo(has_ego);
  };

  useEffect(() => {
    if (!loadingInfo) {
      setLoadingInfo(true);

      if (hasEgo) {
        Promise.all([
          fetchWorldInfo(),
          fetchVehicleLocations(),
          fetchSensors(),
        ]).finally(() => {
          setLoadingInfo(false);
        });
      } else {
        Promise.all([fetchWorldInfo(), fetchVehicleLocations()]).finally(() => {
          setLoadingInfo(false);
        });
      }
    }
  }, [loadingInfo, hasEgo]);

  useEffect(() => {
    if (canvasRef.current && mapInfo.spawn_points.length > 0) {
      const ctx = canvasRef.current;
      const spawnPointsData = mapInfo.spawn_points.map((point) => ({
        x: point[0],
        y: point[1],
      }));
      const actorLocationsData = mapInfo.actor_locations.map((location) => ({
        x: location[0],
        y: location[1],
      }));

      if (!chart) {
        const newChart = new Chart(ctx, {
          type: "scatter",
          data: {
            datasets: [
              {
                label: "Spawn Points",
                data: spawnPointsData,
                backgroundColor: "rgba(54, 162, 235, 0.6)", // Blue
                borderColor: "rgba(54, 162, 235, 1)",
                borderWidth: 1,
              },
              {
                label: "Actor Locations",
                data: actorLocationsData,
                backgroundColor: "rgba(255, 99, 132, 0.6)", // Red
                borderColor: "rgba(255, 99, 132, 1)",
                borderWidth: 1,
              },
            ],
          },
          options: {
            scales: {
              x: {
                display: false,
              },
              y: {
                display: false,
              },
            },
            plugins: {
              legend: {
                display: false,
              },
              tooltip: {
                enabled: false,
              },
            },
            elements: {
              point: {
                radius: 5,
              },
            },
            layout: {
              padding: {
                top: 10,
                right: 10,
                bottom: 10,
                left: 10,
              },
            },
          },
        });
        setChart(newChart);
      } else {
        chart.data.datasets[0].data = spawnPointsData;
        chart.data.datasets[1].data = actorLocationsData;
        chart.update();
      }
    }
  }, [mapInfo, chart]);

  useEffect(() => {
    checkIfEgoExists();
    fetchMapInfo();
  }, []);

  return (
    <main>
      <div className="header">
        <h1>CARLA Web UI</h1>
      </div>
      <div className="body">
        <div className="left-controls">
          <div className="world-info">
            <h2>World Info</h2>
            <p>Map: {worldInfo.map}</p>
            <p>Precipitation: {worldInfo.precipitation}</p>
            <p>Wind Intensity: {worldInfo.wind_intensity}</p>
            <p>Number of Vehicles: {worldInfo.num_vehicles}</p>
          </div>
          <WeatherSelect />
          <MapSelect />
          <VehiclesNumberInput />
          <RemoveLayers />
        </div>
        <div className="middle">
          {hasEgo && (
            <>
              <div className="map-graph">
                <canvas ref={canvasRef}></canvas>
              </div>
              <div className="ego-sensors">
                <h2>Ego Sensors</h2>
                <p>GNSS Data: {JSON.stringify(sensors.gnss_data)}</p>
                <img
                  className="carla-image"
                  src={`data:image/png;base64,${sensors.image}`}
                />
              </div>
            </>
          )}
        </div>
        <div className="right-controls">
          <EgoButtonGroup
            hasEgo={hasEgo}
            setHasEgo={(value) => setHasEgo(value)}
          />
          <RandomButtonGroup />
          {alert && <Alert severity="error">Error removing all vehicles</Alert>}
          <Button
            sx={{
              backgroundColor: "#f44336",
              color: "#fff",
              "&:hover": {
                backgroundColor: "#d32f2f",
              },
            }}
            onClick={removeAllActors}
          >
            Remove All Vehicles
          </Button>
        </div>
      </div>
    </main>
  );
}

export default App;
