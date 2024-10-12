import React, { useEffect, useState } from "react";
import { Stack, ToggleButton, ToggleButtonGroup } from "@mui/material";

import { useDispatch, useSelector } from "react-redux";
import { setControls, setIsLevelLine } from "../store/controlsReducer";

export const Controls = ({ direction, handleDirectionChange, disabled }) => {
  const [activeButtons, setActiveButtons] = useState([]);

  let controls = useSelector((state) => state.controls);
  const dispatch = useDispatch();

  // tracking active graph modes
  useEffect(() => {
    let newActiveButtons = [];
    for (const [ctrl, flag] of Object.entries(controls)) {
      if (flag) {
        newActiveButtons.push(ctrl);
      }
    }
    setActiveButtons(newActiveButtons);
  }, [controls]);

  // storing the state of graph modes
  const handleControls = (event, newActiveButtons) => {
    let newControls = {};
    for (const btn of newActiveButtons) {
      newControls[btn] = true;
    }
    dispatch(setControls(newControls));

    if (newActiveButtons.includes("decibels")) {
      dispatch(setIsLevelLine(false));
    }
  };

  return (
    <Stack direction="row" spacing={2}>
      <ToggleButtonGroup
        exclusive
        color="primary"
        value={direction}
        onChange={handleDirectionChange}
        disabled={disabled}
      >
        <ToggleButton value="azimuth">Азимут</ToggleButton>
        <ToggleButton value="range">Дальность</ToggleButton>
      </ToggleButtonGroup>

      <ToggleButtonGroup
        value={activeButtons}
        onChange={handleControls}
        color="primary"
        disabled={disabled}
      >
        <ToggleButton selected={controls.decibels} value="decibels">
          Децибелы
        </ToggleButton>

        <ToggleButton selected={controls.interpolation} value="interpolation">
          Интерполяция
        </ToggleButton>

        <ToggleButton
          selected={controls.levelLine}
          disabled={controls.decibels}
          value="levelLine"
        >
          Линия уровня
        </ToggleButton>
      </ToggleButtonGroup>
    </Stack>
  );
};
