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

interface WorldInfo {
  map: string;
  precipitation: number;
  wind_intensity: number;
  num_actors: number;
}

interface Point {
  x: number;
  y: number;
}

function App() {
  const [mapInfo, setMapInfo] = useState({
    size: [] as number[],
    spawn_points: [] as Point[],
    actor_locations: [] as Point[],
  });
  const [chart, setChart] = useState<Chart | null>(null);
  const [alert, setAlert] = useState(false);
  const [worldInfo, setWorldInfo] = useState<WorldInfo>({
    map: "Town10",
    precipitation: 0,
    wind_intensity: 0,
    num_actors: 0,
  });

  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  const fetchWorldInfo = async () => {
    const res = await fetch(`${baseUrl}/api/carla/world_info`, {
      method: "GET",
    });
    const { map, precipitation, wind_intensity, num_actors } = await res.json();
    setWorldInfo({
      map: map.slice(0, 6),
      precipitation,
      wind_intensity,
      num_actors,
    });
  };

  const fetchMapInfo = async () => {
    const res = await fetch(`${baseUrl}/api/carla/map_info`, {
      method: "GET",
    });
    const { size, spawn_points, actor_locations } = await res.json();
    setMapInfo({
      size,
      spawn_points,
      actor_locations,
    });
  };

  const removeAllActors = async () => {
    const res = await fetch(`${baseUrl}/api/carla/destroy/all`, {
      method: "DELETE",
    });
    const { error, success } = await res.json();
    setAlert(error || !success);
  };

  useEffect(() => {
    fetchWorldInfo();
    fetchMapInfo();
  }, []);

  useEffect(() => {
    if (canvasRef.current && mapInfo.spawn_points.length > 0) {
      const ctx = canvasRef.current;
      const spawnPointsData = mapInfo.spawn_points.map((point) => ({ x: point.x, y: point.y }));
      const actorLocationsData = mapInfo.actor_locations.map((location) => ({ x: location.x, y: location.y }));

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
                type: 'linear',
                position: 'bottom',
                title: {
                  display: true,
                  text: 'X Coordinate',
                },
                min: 0,
                max: mapInfo.size[0],
              },
              y: {
                title: {
                  display: true,
                  text: 'Y Coordinate',
                },
                min: 0,
                max: mapInfo.size[1],
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

  return (
    <main>
      <div className="header">
        <h1>CARLA Web UI</h1>
      </div>
      <div className="body">
        <div className="left-controls">
          <WeatherSelect />
          <MapSelect />
          <RemoveLayers />
        </div>
        <div className="middle">
          <div className="world-info">
            <h2>World Info</h2>
            <p>Map: {worldInfo.map}</p>
            <p>Precipitation: {worldInfo.precipitation}</p>
            <p>Wind Intensity: {worldInfo.wind_intensity}</p>
            <p>Number of Actors: {worldInfo.num_actors}</p>
          </div>
          <div className="map-graph">
            <canvas ref={canvasRef}></canvas>
          </div>
        </div>
        <div className="right-controls">
          <EgoButtonGroup />
          <RandomButtonGroup />
          {alert && <Alert severity="error">Error removing all actors</Alert>}
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
            Remove All Actors
          </Button>
        </div>
      </div>
    </main>
  );
}

export default App;
