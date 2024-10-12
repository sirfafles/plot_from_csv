import React, { useEffect, useState } from "react";
import { Stack, IconButton } from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import { DataGrid } from "@mui/x-data-grid";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { ruRU } from "@mui/material/locale";
import styles from "./RowTable.module.css";

const theme = createTheme(ruRU);

const columns = [
  { field: "id", headerName: "№", width: 70 },
  { field: "value", headerName: "Значение", width: 95 },
];

export const RowTable = ({ rows, visible, setVisible, handleRowChange }) => {
  const rootStyle = [styles.container];
  if (visible) {
    rootStyle.push(styles.active);
  }

  return (
    <Stack spacing={1} className={rootStyle.join(" ")}>
      <IconButton
        onClick={() => setVisible(false)}
        sx={{ zIndex: 110, position: "absolute", top: 0, right: 0 }}
      >
        <CloseIcon />
      </IconButton>
      <ThemeProvider theme={theme}>
        <DataGrid
          sx={{
            width: "200px",
            border: "none",
            "& .MuiDataGrid-cell:focus": {
              outline: " none",
            },
          }}
          disableColumnMenu
          pageSize={Infinity}
          hideFooter
          disableMultipleSelection
          columns={columns}
          rows={rows}
          onRowSelectionModelChange={([selectedRowIndex]) => {
            handleRowChange(selectedRowIndex);
          }}
        />
      </ThemeProvider>
    </Stack>
  );
};
