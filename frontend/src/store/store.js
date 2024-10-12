import { configureStore, combineReducers } from "@reduxjs/toolkit";
import {
  persistStore,
  persistReducer,
  FLUSH,
  REHYDRATE,
  PAUSE,
  PERSIST,
  PURGE,
  REGISTER,
} from "redux-persist";
import storage from "redux-persist/lib/storage";

import controlsReducer from "./controlsReducer";
import fileNameReducer from "./fileNameReducer";
import tableRowsReducer from "./tableRowsReducer";

const persistConfig = {
  key: "root",
  storage,
};

const rootReducer = combineReducers({
  controls: controlsReducer,
  fileName: fileNameReducer,
  tableRows: tableRowsReducer,
});

const persistedReducer = persistReducer(persistConfig, rootReducer);

const store = configureStore({
  reducer: persistedReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
      },
    }),
});

export const persistor = persistStore(store);
export default store;
