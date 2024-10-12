import axios from "axios";
import env from "react-dotenv";

export const fileAPI = axios.create({
  baseURL: env.FILE_API_URL,
});

export const plotAPI = axios.create({
  baseURL: env.FILE_PLOT_URL,
});
