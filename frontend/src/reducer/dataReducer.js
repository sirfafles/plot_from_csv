import { ACTIONS } from "./ACTIONS";

const initialState = {
  row: null,
  decibels: null,
  interpolation: null,
  decibelsInterpolation: null,
  levelLine: null,
  precision: null
};

export const dataInitializer = (initialValue = initialState) => initialValue;

export function dataReducer(state, { type, graph }) {
  switch (type) {
    case ACTIONS.RESET_DATA:
      return initialState;

    case ACTIONS.SET_ROW:
      return { ...state, row: graph };

    case ACTIONS.SET_DECIBELS:
      return { ...state, decibels: graph };

    case ACTIONS.SET_INTERPOLATION:
      return { ...state, interpolation: graph };

    case ACTIONS.SET_DECIBELS_INTERPOLATION:
      return { ...state, decibelsInterpolation: graph };

    case ACTIONS.SET_LEVEL_LINE:
      return { ...state, levelLine: graph };

    case ACTIONS.SET_PRECISION:
      return {...state, precision: graph}

    default:
      throw new Error(`Unknown action type: ${type}`);
  }
}
