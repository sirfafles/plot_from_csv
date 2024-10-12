import { fileAPI } from "./APIConfig";

export function deleteFile(filename) {
  return fileAPI.delete("/delete/", { params: { filename: filename } });
}
