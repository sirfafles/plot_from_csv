import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  nameToSend: "",
  displayName: "",
};

const slice = createSlice({
  name: "fileName",
  initialState,
  reducers: {
    setNameToSend: (state, action) => {
      state.nameToSend = action.payload;
    },

    setDisplayName: (state, action) => {
      state.nameToSend = action.payload;
    },

    resetFileName: (state) => {
      state = initialState;
    },
  },
});

export const { setNameToSend, setDisplayName, resetFileName } = slice.actions;

export default slice.reducer;
