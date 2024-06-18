import { useEffect, useRef, useState } from "react";
import "./App.css";
import { baseUrl } from "./services/api";
import WeatherSelect from "./components/WeatherSelect/WeatherSelect";
import MapSelect from "./components/MapSelect/MapSelect";
import RemoveLayers from "./components/RemoveLayers/RemoveLayers";
import EgoButtonGroup from "./components/EgoButtonGroup/EgoButtonGroup";
import Chart from "chart.js/auto";
import VehiclesNumberInput from "./components/VehiclesNumberInput/VehiclesNumberInput";
import { MapInfo } from "./types/MapInfo";
import { Sensors } from "./types/Sensors";
import { WorldInfo } from "./types/WorldInfo";

function App() {
  const [mapInfo, setMapInfo] = useState<MapInfo>({
    size: [] as number[],
    spawn_points: [] as number[][],
    sign_locations: [] as number[][],
    vehicle_locations: [] as number[][],
    ego_location: [] as number[],
    spectator_location: [] as number[],
  });
  const [chart, setChart] = useState<Chart | null>(null);
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
    const {
      sign_locations,
      vehicle_locations,
      ego_location,
      spectator_location,
    } = await res.json();
    setMapInfo((prev) => ({
      ...prev,
      sign_locations,
      vehicle_locations,
      ego_location,
      spectator_location,
    }));
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
      const signLocationsData = mapInfo.sign_locations.map((point) => ({
        x: point[0],
        y: point[1],
      }));
      const vehicleLocationsData = mapInfo.vehicle_locations.map((point) => ({
        x: point[0],
        y: point[1],
      }));
      const egoLocationData = Array.of({
        x: mapInfo.ego_location[0],
        y: mapInfo.ego_location[1],
      });
      const spectatorLocationData = Array.of({
        x: mapInfo.spectator_location[0],
        y: mapInfo.spectator_location[1],
      });

      if (!chart) {
        const newChart = new Chart(ctx, {
          type: "scatter",
          data: {
            datasets: [
              {
                label: "Spectator Location", // yellow
                data: spectatorLocationData,
                backgroundColor: "rgba(255, 255, 0, 0.8)",
                borderColor: "rgba(255, 255, 0, 1)",
                borderWidth: 1,
              },
              {
                label: "Ego Location", // red
                data: egoLocationData,
                backgroundColor: "rgba(255, 0, 0, 0.8)",
                borderColor: "rgba(255, 0, 0, 1)",
                borderWidth: 1,
              },
              {
                label: "Vehicle Locations", // green
                data: vehicleLocationsData,
                backgroundColor: "rgba(0, 255, 0, 0.8)",
                borderColor: "rgba(0, 255, 0, 1)",
                borderWidth: 1,
              },
              {
                label: "Sign Locations", // brown
                data: signLocationsData,
                backgroundColor: "rgba(100, 65, 23, 0.8)",
                borderColor: "rgba(0, 0, 0, 1)",
                borderWidth: 1,
              },
              {
                label: "Spawn Points", // cyan
                data: spawnPointsData,
                backgroundColor: "rgba(0, 255, 255, 0.2)",
                borderColor: "rgba(0, 0, 0, 1)",
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
                display: true,
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
        chart.data.datasets[0].data = spectatorLocationData;
        chart.data.datasets[1].data = egoLocationData;
        chart.data.datasets[2].data = vehicleLocationsData;
        chart.data.datasets[3].data = signLocationsData;
        chart.data.datasets[4].data = spawnPointsData;
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
            <h3>World Info</h3>
            <p>Map: {worldInfo.map}</p>
            <p>Precipitation: {worldInfo.precipitation}</p>
            <p>Wind Intensity: {worldInfo.wind_intensity}</p>
            <p>Number of Vehicles: {worldInfo.num_vehicles}</p>
          </div>

          <WeatherSelect />

          <MapSelect />

          <VehiclesNumberInput />

          <RemoveLayers />

          <EgoButtonGroup
            hasEgo={hasEgo}
            setHasEgo={(value) => setHasEgo(value)}
            mapInfo={mapInfo}
            setMapInfo={(value) => setMapInfo(value)}
          />
        </div>

        <div className="middle">
          <div className="map-graph">
            <canvas ref={canvasRef}></canvas>
          </div>
          {hasEgo && (
            <div className="ego-sensors">
              <h2>Ego Sensors</h2>
              {sensors.gnss_data?.lat && (
                <p>
                  Latitude: {sensors.gnss_data.lat} | Longitude:{" "}
                  {sensors.gnss_data.lon}
                </p>
              )}
              <img
                className="carla-image"
                src={`data:image/png;base64,${sensors.image}`}
              />
            </div>
          )}
        </div>
      </div>
    </main>
  );
}

export default App;
