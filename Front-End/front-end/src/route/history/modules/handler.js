import {
    HISTORY_DATA,
    SUCCESS,
    PENDING,
    ERROR
} from "./actions"

import update from "immutability-helper"

export const actionHandlers = {};
actionHandlers[HISTORY_DATA] = handleHistoryData;
actionHandlers[SUCCESS] = handleSuccess;
actionHandlers[PENDING] = handlePending;
actionHandlers[ERROR] = handleError

function handleHistoryData(state, action) {
    return update(state, {
        historyData: { $set: action.payload }
    })
}

function handleSuccess(state, action) {
    return update(state, {
        success: { $set: action.payload }
    })
}

function handlePending(state, action) {
    return update(state, {
        pending: { $set: action.payload }
    })
}

function handleError(state, action) {
    return update(state, {
        error: { $set: action.payload }
    })
}