import { Stack, TextField, Button } from "@mui/material";

export const ResolutionControls = ({
  disabled,
  direction,
  selectedRow,
  numberInputs,
  setNumberInputs,
  getPrecision,
}) => {
  const handleNumberInput = (event) => {
    const id = event.target.id;
    const value = event.target.value;
    let newInputs = numberInputs;
    newInputs[id] = value;
    setNumberInputs(newInputs);
  };

  if (direction === "azimuth") {
    return (
      <Stack direction="row" spacing={1}>
        <TextField
          disabled={!selectedRow}
          sx={{ width: "24ch" }}
          type="number"
          defaultValue={50}
          label="Скорость"
          onChange={handleNumberInput}
          id="speed"
          size="small"
        />
        <TextField
          disabled={!selectedRow}
          sx={{ width: "24ch" }}
          type="number"
          defaultValue={2_000}
          label="ЧПИ"
          onChange={handleNumberInput}
          id="prf"
          size="small"
        />

        <Button variant="outlined" onClick={getPrecision} disabled={disabled}>
          Рассчитать
        </Button>
      </Stack>
    );
  } else {
    return (
      <Stack direction="row" spacing={1}>
        <TextField
          disabled={!selectedRow}
          sx={{ width: "24ch" }}
          type="number"
          defaultValue={1_250_000_000}
          label="Частота АЦП"
          id="deltaf"
          onChange={handleNumberInput}
          size="small"
        />

        <Button variant="outlined" onClick={getPrecision} disabled={disabled}>
          Рассчитать
        </Button>
      </Stack>
    );
  }
};
