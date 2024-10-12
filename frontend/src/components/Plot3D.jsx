import React, { useEffect } from "react";
import Plot from "react-plotly.js";
import useLocalStorage from "../hooks/useLocalStorage";
import { get3DPlot } from "../API/get3DPlot";

export const Plot3D = ({ styles, filename }) => {
  const [data, setData] = useLocalStorage([], "data3D");

  //get 3d plot
  useEffect(() => {
    if (!filename) {
      return;
    }
    const params = {
      filename: filename,
    };
    get3DPlot(params).then(({ matrixSurface, DBMatrixSurface }) => {
      setData([matrixSurface, DBMatrixSurface]);
    });
  }, [filename]);

  const layout = {
    title: "Уголковый отражатель",
    scene1: {
      domain: {
        x: [0.0, 0.49],
        y: [0, 1.2],
      },
    },
    scene2: {
      domain: {
        x: [0.51, 1],
        y: [0, 1.0],
      },
    },
    showlegend: false,
    annotations: [
      {
        text: "Абсолютные значения",
        font: {
          size: 16,
        },
        showarrow: false,
        align: "center",
        x: 0.13, //position in x domain
        y: 1, //position in y domain
        xref: "paper",
        yref: "paper",
      },
      {
        text: "Значения в децибелах",
        font: {
          size: 16,
        },
        showarrow: false,
        align: "center",
        x: 0.9, //position in x domain
        y: 1, // position in y domain
        xref: "paper",
        yref: "paper",
      },
    ],
  };

  return <Plot className={styles} useResizeHandler={true} data={data} layout={layout} />;
};
