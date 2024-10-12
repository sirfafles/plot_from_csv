import { fileAPI } from "./APIConfig";

export function uploadFile(file) {
  const formData = new FormData();
  formData.append("file", file);
  return fileAPI.post("/upload/", formData);
}
