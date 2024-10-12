import React, { useState } from "react";
import { Button, Stack, CircularProgress } from "@mui/material";
import { uploadFile } from "../API/uploadFile";
import { getRows } from "../API/getRows";

export const UploadForm = ({ drawOnUpload }) => {
  const [isInProgress, setIsInProgress] = useState(false);
  const handleFileUpload = async (event) => {
    
    const file = event.target.files[0];
    if (!file) {
      setIsInProgress(false);
      return;
    }

    try {
      setIsInProgress(true);
      let uploadTimer = setTimeout(() => {
        alert("Что-то пошло не так. Повторите попытку");
      }, 20000);
      
      const response = await uploadFile(file);
      const filename = await response.data.filename;
      const { azimuthRows, rangeRows } = await getRows(filename);
      
      clearTimeout(uploadTimer);

      drawOnUpload(encodeURIComponent(filename), rangeRows, azimuthRows);
    } catch (error) {
      console.log(error);
    } finally {
      setIsInProgress(false);
    }
  };

  return (
    <Stack
      direction="row"
      spacing={2}
      sx={{ display: "inline-flex", alignItems: "center" }}
    >
      <Button variant="contained" component="label">
        <input
          id="inputFiles"
          type="file"
          accept=".tiff,.tif,.csv"
          onChange={handleFileUpload}
          hidden
        />
        Загрузить
      </Button>
      {isInProgress && <CircularProgress />}
    </Stack>
  );
};
