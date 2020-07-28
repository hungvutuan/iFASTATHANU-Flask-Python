import { combineReducers } from "redux"
import liveReducer from "../route/live/modules"
import historyReducer from "../route/history/modules"
import mainReducer from "../route/main/modules"

export default function makeRootReducer() {
    return combineReducers({
        liveData: liveReducer,
        historyData: historyReducer,
        mainData: mainReducer,

    })
}