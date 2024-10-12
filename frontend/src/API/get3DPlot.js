import { plotAPI } from "./APIConfig";

export async function get3DPlot(params) {
  try {
    const response = await plotAPI.get(`/3d-plot/`, {
      params: { ...params },
    });

    const matrix = {
      colorscale: "Jet",
      z: response.data.z_data,
      type: "surface",
      scene: "scene1",
      showscale: false,
    };
    const DBMatrix = {
      colorscale: "Jet",
      z: response.data.z_data_db,
      type: "surface",
      scene: "scene2",
    };

    return { matrixSurface: matrix, DBMatrixSurface: DBMatrix };
  } catch (error) {
    if (error?.response?.data?.detail) {
      // alert(error.response.data.detail);
    }
    console.log(error);
    return {};
  }
}
