import { plotAPI } from "./APIConfig";
import { plotNames, plotColors } from "../constants/plotConstants";

export async function getPlot(plotType, params) {
  try {
    const response = await plotAPI.get(`/${plotType}/`, {
      params: { ...params },
    });
    let { x_range, x_data, resolution_val } = response.data;
    resolution_val = resolution_val?.toPrecision(3);
    return {
      x: x_range,
      y: x_data,
      type: "scatter",
      mode: `${resolution_val ? "" : "lines"}`,
      name: plotNames[plotType] + ` ${resolution_val ? resolution_val : ""}`,
      marker: { color: plotColors[plotType] },
      text: resolution_val
        ? `Радиометрическое разрешение: ${resolution_val}`
        : "",
    };
  } catch (error) {
    if (error?.response?.data?.detail) {
      // alert(error.response.data.detail
    }
    console.log(error);
    return {};
  }
}
