export const plotQueryTypes = {
  row: "row",
  decibels: "decibels",
  interpolation: "interpolation",
  decibelsInterpolation: "decibels-interpolation",
  levelLine: "level-line",
  resolution: "radiometric-resolution",
};

export const plotNames = {
  row: "График",
  decibels: "Децибелы",
  interpolation: "Интерполяция",
  "decibels-interpolation": "Интерполяция",
  "level-line": "Линия уровня",
  "radiometric-resolution": "Разрешение",
  range: "Дальность",
  azimuth: "Азимут",
};

export const plotColors = {
  row: "#1f77b4",
  decibels: "#1f77b4",
  interpolation: "#ffb74d",
  "decibels-interpolation": "#ffb74d",
  "level-line": "#404040",
  "radiometric-resolution": "#f70000",
};

export const plotLayout = {
  showlegend: true,
  legend: { itemwidth: 30 },
  xaxis: {
    title: {
      text: "Отсчет",
    },
    linecolor: "#6e6e6e",
    linewidth: 1,
    mirror: true,
  },
  yaxis: {
    title: {
      text: "Амплитуда",
    },
    linecolor: "#6e6e6e",
    linewidth: 1,
    mirror: true,
  },
};
