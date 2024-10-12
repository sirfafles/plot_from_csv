import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  display: [],
  azimuth: [],
  range: [],
};

const slice = createSlice({
  name: "tableRows",
  initialState,
  reducers: {
    resetTableRows: (state, action) => {
      state = initialState;
    },

    setTableRows: (state, action) => {
      state.azimuth = action.payload.azimuth;
      state.range = action.payload.range;
      state.azimuth = action.payload.azimuth;
    },

    setDisplayRows: (state, action) => {
      state.display = action.payload;
    },

    setAzimuthRows: (state, action) => {
      state.azimuth = action.payload;
    },

    setRangeRows: (state, action) => {
      state.range = action.payload;
    },
  },
});

export const {
  setTableRows,
  setDisplayRows,
  setAzimuthRows,
  setRangeRows,
  resetTableRows,
} = slice.actions;

export default slice.reducer;
