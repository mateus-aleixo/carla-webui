import Button from "@mui/material/Button";
import { Modal, Box, Alert } from "@mui/material";
import { useState } from "react";
import { baseUrl } from "../../services/api";
import { MapInfo } from "../../types/MapInfo";
import RandomButtonGroup from "../RandomButtonGroup/RandomButtonGroup";

export default function EgoButtonGroup({
  hasEgo,
  setHasEgo,
  mapInfo,
  setMapInfo,
}: {
  hasEgo: boolean;
  setHasEgo: (hasEgo: boolean) => void;
  mapInfo: MapInfo;
  setMapInfo: (mapInfo: MapInfo) => void;
}) {
  const [open, setOpen] = useState(false);
  const [alerts, setAlerts] = useState({
    add: false,
    remove: false,
  });
  const [alert, setAlert] = useState(false);

  const addEgo = async (ego: string) => {
    const res = await fetch(`${baseUrl}/api/carla/ego/add`, {
      method: "POST",
      body: JSON.stringify({ ego: "vehicle." + ego }),
      headers: {
        "Content-Type": "application/json",
      },
    });

    const { error, success } = await res.json();
    const alert = error || !success;

    setAlerts({ ...alerts, add: alert });
    setHasEgo(!alert);
    setOpen(false);
  };

  const removeEgo = async () => {
    const res = await fetch(`${baseUrl}/api/carla/ego/remove`, {
      method: "DELETE",
    });

    const { error, success } = await res.json();
    const alert = error || !success;

    setAlerts({ ...alerts, remove: alert });
    setHasEgo(alert);
  };

  const fetchMapInfo = async () => {
    const res = await fetch(`${baseUrl}/api/carla/map_info`, {
      method: "GET",
    });
    const { size, spawn_points } = await res.json();
    setMapInfo({ ...mapInfo, size, spawn_points });
  };

  const handleAdd = () => {
    setOpen(true);
    fetchMapInfo();
  };

  const removeAllActors = async () => {
    const res = await fetch(`${baseUrl}/api/carla/destroy/all`, {
      method: "DELETE",
    });
    const { error, success } = await res.json();
    setAlert(error || !success);
  };

  return (
    <Box
      sx={{
        minWidth: 100,
        display: "flex",
        justifyContent: "center",
        alignItems: "stretch",
        flexDirection: "column",
        gap: 1,
      }}
    >
      <Modal open={open} onClose={() => setOpen(false)}>
        <Box
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr 1fr",
            justifyItems: "center",
            alignItems: "stretch",
            gap: 10,
            padding: 10,
            backgroundColor: "white",
            borderRadius: 5,
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            width: "80%",
            height: "80%",
            overflowY: "scroll",
          }}
          sx={{
            img: {
              border: "2px solid #000",
              width: 300,
              objectFit: "contain",
              cursor: "pointer",
            },
          }}
        >
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/audi_a2.webp"
            onClick={() => addEgo("audi.a2")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/audi_etron.webp"
            onClick={() => addEgo("audi.etron")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/audi_tt.webp"
            onClick={() => addEgo("audi.tt")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/bmw_grandtourer.webp"
            onClick={() => addEgo("bmw.grandtourer")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/chevrolet_impala.webp"
            onClick={() => addEgo("chevrolet.impala")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/citroen_c3.webp"
            onClick={() => addEgo("citroen.c3")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/dodge_charger_2020.webp"
            onClick={() => addEgo("dodge.charger_2020")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/dodge_charger_police.webp"
            onClick={() => addEgo("dodge.charger_police")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/dodge_charger_police_2020.webp"
            onClick={() => addEgo("dodge.charger_police_2020")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/ford_crown.webp"
            onClick={() => addEgo("ford.crown")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/ford_mustang.webp"
            onClick={() => addEgo("ford.mustang")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/jeep_wrangler_rubicon.webp"
            onClick={() => addEgo("jeep.wrangler_rubicon")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/lincoln_mkz_2017.webp"
            onClick={() => addEgo("lincoln.mkz_2017")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/lincoln_mkz_2020.webp"
            onClick={() => addEgo("lincoln.mkz_2020")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/mercedes_coupe.webp"
            onClick={() => addEgo("mercedes.coupe")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/mercedes_coupe_2020.webp"
            onClick={() => addEgo("mercedes.coupe_2020")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/micro_microlino.webp"
            onClick={() => addEgo("micro.microlino")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/mini_cooper_s.webp"
            onClick={() => addEgo("mini.cooper_s")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/mini_cooper_s_2021.webp"
            onClick={() => addEgo("mini.cooper_s_2021")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/nissan_micra.webp"
            onClick={() => addEgo("nissan.micra")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/nissan_patrol.webp"
            onClick={() => addEgo("nissan.patrol")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/nissan_patrol_2021.webp"
            onClick={() => addEgo("nissan.patrol_2021")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/seat_leon.webp"
            onClick={() => addEgo("seat.leon")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/tesla_model3.webp"
            onClick={() => addEgo("tesla.model3")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/toyota_prius.webp"
            onClick={() => addEgo("toyota.prius")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/carlamotors_carlacola.webp"
            onClick={() => addEgo("carlamotors.carlacola")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/carlamotors_european_hgv.webp"
            onClick={() => addEgo("carlamotors.european_hgv")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/carlamotors_firetruck.webp"
            onClick={() => addEgo("carlamotors.firetruck")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/tesla_cybertruck.webp"
            onClick={() => addEgo("tesla.cybertruck")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/ford_ambulance.webp"
            onClick={() => addEgo("ford.ambulance")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/mercedes_sprinter.webp"
            onClick={() => addEgo("mercedes.sprinter")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/volkswagen_t2.webp"
            onClick={() => addEgo("volkswagen.t2")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/volkswagen_t2_2021.webp"
            onClick={() => addEgo("volkswagen.t2_2021")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/mitsubishi_fusorosa.webp"
            onClick={() => addEgo("mitsubishi.fusorosa")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/harley-davidson_low_rider.webp"
            onClick={() => addEgo("harley-davidson.low_rider")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/kawasaki_ninja.webp"
            onClick={() => addEgo("kawasaki.ninja")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/vespa_zx125.webp"
            onClick={() => addEgo("vespa.zx125")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/yamaha_yzf.webp"
            onClick={() => addEgo("yamaha.yzf")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/bh_crossbike.webp"
            onClick={() => addEgo("bh.crossbike")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/diamondback_century.webp"
            onClick={() => addEgo("diamondback.century")}
          />
          <img
            src="https://carla.readthedocs.io/en/latest/img/catalogue/vehicles/gazelle_omafiets.webp"
            onClick={() => addEgo("gazelle.imafiets")}
          />
        </Box>
      </Modal>

      {alerts.add && (
        <Alert severity="error">
          EGO Vehicle already exists. Please remove it first.
        </Alert>
      )}
      {alerts.remove && (
        <Alert severity="error">
          EGO Vehicle does not exist. Please add it first.
        </Alert>
      )}

      <Button disabled={hasEgo} variant="contained" onClick={handleAdd}>
        Add EGO Vehicle
      </Button>

      <Button disabled={!hasEgo} variant="contained" onClick={removeEgo}>
        Remove EGO Vehicle
      </Button>

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
    </Box>
  );
}
