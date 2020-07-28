import { post, deleted, get, put } from "../../../ultis/index"
import { edgeAPIs } from "../../../config"

export const MAIN_DATA = "MAIN_DATA"
export const SUCCESS = "SUCCESS"
export const PENDING = "PENDING"
export const ERROR = "ERROR"

function mainData(data) {
    return {
        type: MAIN_DATA,
        payload: data
    }
}

function success(isSuccess) {
    return {
        type: SUCCESS,
        payload: isSuccess
    }
}

function pending(isPending) {
    return {
        type: PENDING,
        payload: isPending
    }
}

function error(isError) {
    return {
        type: ERROR,
        payload: isError
    }
}

export function getAllMainData() {
    return dispatch => {
        dispatch(pending(true))
        get(edgeAPIs.server()).then(res => {
            dispatch(mainData(res))
        }).catch(err => {
            dispatch(error(err))
        }).finally(() => dispatch(pending(false)))
    }

}

export function updateMainData(mainDto) {
    return dispatch => {
        dispatch(pending(true))
        put(edgeAPIs.server(), mainDto).then(res => {
            dispatch(mainData(res))
        }).catch(err => {
            dispatch(error(err))
        }).finally(() => dispatch(pending(false)))
    }

}

export function deleteMainData(id) {
    return dispatch => {
        dispatch(pending(true))
        deleted(edgeAPIs.server(), id).then(res => {
            dispatch(mainData(res))
        }).catch(err => {
            dispatch(error(err))
        }).finally(() => dispatch(pending(false)))
    }

}

export function addNewData(mainDto) {
    return dispatch => {
        dispatch(pending(true))
        post(edgeAPIs.server(), mainDto).then(res => {
            dispatch(mainData(res))
        }).catch(err => {
            dispatch(error(err))
        }).finally(() => dispatch(pending(false)))
    }

}