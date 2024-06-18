from api.routes import create_api
from flask import Flask
from flask_caching import Cache
import pytest


"""Tests for the API."""


@pytest.fixture
def client():
    app = Flask(__name__)
    cache = Cache(config={"CACHE_TYPE": "SimpleCache"})
    cache.init_app(app)
    api = create_api(cache)
    app.register_blueprint(api, url_prefix="/api/carla")
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_world_info(client):
    response = client.get("/api/carla/world_info")
    assert response.status_code == 200
    data = response.get_json()
    assert "map" in data
    assert "precipitation" in data
    assert "wind_intensity" in data
    assert "num_vehicles" in data


def test_locations(client):
    response = client.get("/api/carla/vehicles")
    assert response.status_code == 200
    data = response.get_json()
    assert "sign_locations" in data
    assert "vehicle_locations" in data
    assert "ego_location" in data
    assert "spectator_location" in data


def test_map_info(client):
    response = client.get("/api/carla/map_info")
    assert response.status_code == 200
    data = response.get_json()
    assert "size" in data
    assert "spawn_points" in data


def test_has_ego(client):
    response = client.get("/api/carla/ego/vehicle")
    assert response.status_code == 200
    data = response.get_json()
    assert "has_ego" in data


def test_set_weather(client):
    response = client.post("/api/carla/weather", json={"weather": "ClearNoon"})
    assert response.status_code == 200
    data = response.get_json()
    assert "success" in data


def test_set_invalid_weather(client):
    response = client.post("/api/carla/weather", json={"weather": "InvalidWeather"})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_set_map(client):
    response = client.post("/api/carla/map", json={"map": "Town01"})
    assert (
        response.status_code == 200 or response.status_code == 400
    )  # Depending on initial map
    data = response.get_json()
    assert "success" in data or "error" in data


def test_set_layers_all(client):
    response = client.post("/api/carla/layers", json={"layers": {"All": True}})
    assert response.status_code == 200
    data = response.get_json()
    assert "success" in data


def test_set_layers_none(client):
    response = client.post("/api/carla/layers", json={"layers": {"NONE": True}})
    assert response.status_code == 200
    data = response.get_json()
    assert "success" in data


def test_add_ego(client):
    response = client.post("/api/carla/ego/add", json={"ego": "vehicle.audi.tt"})
    assert response.status_code == 200
    data = response.get_json()
    assert "success" in data


def test_get_ego_sensors(client):
    response = client.get("/api/carla/ego/sensors")
    assert response.status_code == 200
    data = response.get_json()
    assert "colision_history" in data
    assert "gnss_data" in data
    assert "image" in data


def test_remove_ego(client):
    client.post("/api/carla/ego/add", json={"ego": "vehicle.audi.tt"})
    response = client.delete("/api/carla/ego/remove")
    assert response.status_code == 200
    data = response.get_json()
    assert "success" in data


def test_add_random_vehicle(client):
    response = client.post("/api/carla/random/vehicle/add")
    assert (
        response.status_code == 200 or response.status_code == 404
    )  # Depending on spawn points
    data = response.get_json()
    assert "success" in data or "error" in data


def test_remove_random_vehicle(client):
    client.post("/api/carla/random/vehicle/add")
    response = client.delete("/api/carla/random/vehicle/remove")
    assert response.status_code == 200
    data = response.get_json()
    assert "success" in data


def test_n_vehicles(client):
    response = client.post("/api/carla/random/vehicles", json={"num_vehicles": 5})
    assert response.status_code == 200
    data = response.get_json()
    assert "success" in data


def test_destroy_all(client):
    client.post("/api/carla/random/vehicle/add")
    response = client.delete("/api/carla/destroy/all")
    assert response.status_code == 200
    data = response.get_json()
    assert "success" in data
