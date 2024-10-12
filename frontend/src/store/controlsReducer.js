import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  decibels: false,
  interpolation: false,
  levelLine: false,
};

const slice = createSlice({
  name: "controls",
  initialState,
  reducers: {
    setControls: (state, action) => {
      state.decibels = action.payload.decibels;
      state.interpolation = action.payload.interpolation;
      state.levelLine = action.payload.levelLine;
    },

    resetControls: (state, action) => {
      state.decibels = false;
      state.interpolation = false;
      state.levelLine = false;
    },

    setIsDecibels: (state, action) => {
      state.decibels = action.payload;
    },

    setIsInterpolation: (state, action) => {
      state.interpolation = action.payload;
    },

    setIsLevelLine: (state, action) => {
      state.levelLine = action.payload;
    },
  },
});

export const {
  resetControls,
  setControls,
  setIsDecibels,
  setIsInterpolation,
  setIsLevelLine,
} = slice.actions;

export default slice.reducer;
