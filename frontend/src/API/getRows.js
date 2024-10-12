import { fileAPI } from "./APIConfig";

export async function getRows(filename) {
  const response = await fileAPI.get("/sorted-data/", {
    params: { filename: filename },
  });
  const { azimuthRows, rangeRows } = unwrapRows(response.data);
  return { azimuthRows, rangeRows };
}

function unwrapRows(data) {
  const {
    rg_max_values_sorted,
    rg_indexes_sorted,
    az_max_values_sorted,
    az_indexes_sorted,
  } = data;

  let azimuthRows = new Array(az_indexes_sorted.length);
  let rangeRows = new Array(rg_indexes_sorted.length);

  for (let i = 0; i < az_indexes_sorted.length; i += 1) {
    azimuthRows[i] = {
      id: az_indexes_sorted[i],
      value: az_max_values_sorted[i],
    };
  }

  for (let i = 0; i < rg_indexes_sorted.length; i += 1) {
    rangeRows[i] = {
      id: rg_indexes_sorted[i],
      value: rg_max_values_sorted[i],
    };
  }

  return { azimuthRows, rangeRows };
}
