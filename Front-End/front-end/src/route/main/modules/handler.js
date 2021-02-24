import {
    MAIN_DATA,
    SUCCESS,
    PENDING,
    ERROR
} from "./actions"

import update from "immutability-helper"

export const actionHandlers = {};
actionHandlers[MAIN_DATA] = handleMainData;
actionHandlers[SUCCESS] = handleSuccess;
actionHandlers[PENDING] = handlePending;
actionHandlers[ERROR] = handleError

function handleMainData(state, action) {
    return update(state, {
        mainData: { $set: action.payload }
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