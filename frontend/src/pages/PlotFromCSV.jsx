import React, { useEffect, useMemo, useState, useReducer } from "react";
import Plot from "react-plotly.js";
import TableRowsIcon from "@mui/icons-material/TableRows";
import { Stack, TextField, Button, IconButton } from "@mui/material";

//constants
import {
  plotLayout,
  plotNames,
  plotQueryTypes,
} from "../constants/plotConstants";

//api
import { getPlot } from "../API/getPlot";
import { deleteFile } from "../API/deleteFile";

//store
import { useDispatch, useSelector } from "react-redux";
import { resetControls, setIsLevelLine } from "../store/controlsReducer";
import { resetFileName, setNameToSend } from "../store/fileNameReducer";
import {
  resetTableRows,
  setTableRows,
  setDisplayRows,
} from "../store/tableRowsReducer";
import { ACTIONS } from "../reducer/ACTIONS";
import { dataReducer, dataInitializer } from "../reducer/dataReducer";
import useLocalStorage from "../hooks/useLocalStorage";

//components
import { Popup } from "../UI/Popup/Popup";
import { UploadForm } from "../components/UploadForm";
import { RowTable } from "../components/RowTable/RowTable";
import { Controls } from "../components/Controls";
import { ResolutionControls } from "../components/ResolutionControls";
import { Plot3D } from "../components/Plot3D";
import styles from "../App.module.css";

const PlotFromCSV = () => {
  const [deleteFileDialogOpen, setDeleteFileDialogOpen] = useState(false);
  const [graphLayout, setGraphLayout] = useState(plotLayout);
  const [numberInputs, setNumberInputs] = useState({
    deltaf: 1_250_000_000,
    speed: 50,
    prf: 2000,
  });

  const dispatch = useDispatch();
  const controls = useSelector((state) => state.controls);
  const fileName = useSelector((state) => state.fileName);
  const tableRows = useSelector((state) => state.tableRows);

  const [direction, setDirection] = useLocalStorage(null, "direction");
  const [selectedRow, setSelectedRow] = useLocalStorage(null, "selectedRow");

  const [graphData, dispatchGraphData] = useReducer(
    dataReducer,
    {},
    dataInitializer
  );

  const handleFileDelete = () => {
    dispatch(resetFileName());
    dispatch(resetControls());
    dispatch(resetTableRows());

    setSelectedRow(null);
    setDirection(null);
    dispatchGraphData({ type: ACTIONS.RESET_DATA });

    deleteFile(fileName.nameToSend);
    setDeleteFileDialogOpen(false);
  };

  const handleRowChange = (selectedIndex) => {
    if (!selectedIndex) {
      return;
    }
    setSelectedRow(selectedIndex);
    dispatch(resetControls());
    dispatchGraphData({ type: ACTIONS.RESET_DATA });
  };

  const drawOnUpload = (filename, newRangeRows, newAzimuthRows) => {
    dispatch(resetControls());
    dispatch(setNameToSend(filename));
    dispatch(setTableRows({ azimuth: newAzimuthRows, range: newRangeRows }));
    dispatch(setDisplayRows(newAzimuthRows));

    setDirection("azimuth");
    handleRowChange(newAzimuthRows[0].id);
  };

  //get row
  useEffect(() => {
    if (!selectedRow) {
      return;
    }
    setGraphLayout({
      ...graphLayout,
      title: `${plotNames[direction] ?? direction}`,
    });

    const params = {
      filename: fileName.nameToSend,
      index: selectedRow,
      direction: direction,
    };

    getPlot(plotQueryTypes.row, params).then((newGraph) => {
      dispatchGraphData({ type: ACTIONS.SET_ROW, graph: newGraph });
    });
  }, [selectedRow]);

  //get decibels
  useEffect(() => {
    if (!controls.decibels) {
      return;
    }
    if (graphData.decibels) {
      return;
    }

    const params = {
      filename: fileName.nameToSend,
      index: selectedRow,
      direction: direction,
    };

    getPlot(plotQueryTypes.decibels, params).then((newGraph) => {
      dispatchGraphData({ type: ACTIONS.SET_DECIBELS, graph: newGraph });
    });
  }, [controls.decibels]);

  // get interpolation
  useEffect(() => {
    if (!controls.interpolation) {
      return;
    }

    const params = {
      filename: fileName.nameToSend,
      index: selectedRow,
      direction: direction,
    };

    if (!controls.decibels && !graphData.interpolation) {
      getPlot(plotQueryTypes.interpolation, params).then((newGraph) =>
        dispatchGraphData({ type: ACTIONS.SET_INTERPOLATION, graph: newGraph })
      );
    }

    if (controls.decibels && !graphData.decibelsInterpolation) {
      getPlot(plotQueryTypes.decibelsInterpolation, params).then((newGraph) =>
        dispatchGraphData({
          type: ACTIONS.SET_DECIBELS_INTERPOLATION,
          graph: newGraph,
        })
      );
    }
  }, [controls.interpolation, controls.decibels]);

  //get level line
  useEffect(() => {
    if (!controls.levelLine) {
      return;
    }
    if (!graphData.precision) {
      getPrecision();
    }
    if (graphData.levelLine) {
      return;
    }

    const params = {
      filename: fileName.nameToSend,
      index: selectedRow,
      direction: direction,
    };

    getPlot(plotQueryTypes.levelLine, params).then((newGraph) =>
      dispatchGraphData({ type: ACTIONS.SET_LEVEL_LINE, graph: newGraph })
    );
  }, [controls.levelLine]);

  // get radiometric precision
  const getPrecision = () => {
    const params = {
      filename: fileName.nameToSend,
      index: selectedRow,
      direction: direction,
      deltaf: numberInputs.deltaf,
      speed: numberInputs.speed,
      prf: numberInputs.prf,
    };

    if (!controls.decibels) {
      dispatch(setIsLevelLine(true));
    }

    getPlot(plotQueryTypes.resolution, params).then((newGraph) =>
      dispatchGraphData({ type: ACTIONS.SET_PRECISION, graph: newGraph })
    );
  };

  //drawing
  let graphs = useMemo(() => {
    let newGraphs = [];
    if (controls.decibels) {
      newGraphs.push(graphData.decibels);
    } else {
      newGraphs.push(graphData.row);
    }

    if (controls.interpolation) {
      newGraphs.push(
        controls.decibels
          ? graphData.decibelsInterpolation
          : graphData.interpolation
      );
    }

    if (controls.levelLine) {
      newGraphs.push(graphData.levelLine);
      if (graphData.precision) {
        newGraphs.push(graphData.precision);
      }
    }
    return newGraphs;
  }, [graphData, controls]);

  const handleDirectionChange = (event, newDirection) => {
    if (newDirection === null) {
      return;
    }
    setDirection(newDirection);
    switch (newDirection) {
      case "range":
        dispatch(setDisplayRows(tableRows?.range));
        handleRowChange(tableRows?.range[0].id);
        break;
      case "azimuth":
        dispatch(setDisplayRows(tableRows?.azimuth));
        handleRowChange(tableRows?.azimuth[0].id);
        break;
      default:
        break;
    }
  };

  const [tableVisible, setTableVisible] = useState(false);

  return (
    <Stack className={styles.app} direction="row">
      <Popup
        visible={deleteFileDialogOpen}
        setVisible={setDeleteFileDialogOpen}
      >
        <Stack spacing={1}>
          <p>Удалить файл?</p>
          <Button
            variant="contained"
            onClick={handleFileDelete}
            color="error"
            disabled={!selectedRow}
          >
            Удалить
          </Button>
        </Stack>
      </Popup>

      <RowTable
        rows={tableRows?.display}
        visible={tableVisible}
        setVisible={setTableVisible}
        handleRowChange={handleRowChange}
      />

      <Stack className={styles.wrapper} direction="column" spacing={2}>
        <Stack className={styles.header} direction="row" spacing={2}>
          <IconButton onClick={() => setTableVisible(true)}>
            <TableRowsIcon />
          </IconButton>

          <UploadForm drawOnUpload={drawOnUpload} />

          <Controls
            direction={direction}
            handleDirectionChange={handleDirectionChange}
            disabled={!selectedRow}
          />

          <Button
            variant="contained"
            onClick={() => setDeleteFileDialogOpen(true)}
            color="error"
            disabled={!selectedRow}
          >
            Удалить файл
          </Button>
        </Stack>

        {selectedRow && (
          <Stack className={styles.content} direction="column" spacing={2}>
            <Plot
              useResizeHandler={true}
              className={styles.plot}
              data={graphs}
              layout={graphLayout}
            />

            <Stack direction="row" spacing={2}>
              <ResolutionControls
                disabled={!selectedRow}
                direction={direction}
                selectedRow={selectedRow}
                numberInputs={numberInputs}
                setNumberInputs={setNumberInputs}
                getPrecision={getPrecision}
              />
            </Stack>

            <Plot3D styles={styles.plot3} filename={fileName.nameToSend} />
          </Stack>
        )}
      </Stack>
    </Stack>
  );
};

export default PlotFromCSV;
