import { post, deleted, get, put } from "../../../ultis/index"
import { edgeAPIs } from "../../../config"

export const LIVE_DATA = "LIVE_DATA"
export const SUCCESS = "SUCCESS"
export const PENDING = "PENDING"
export const ERROR = "ERROR"

function liveData(data) {
    return {
        type: LIVE_DATA,
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
            dispatch(liveData(res))
        }).catch(err => {
            dispatch(error(err))
        }).finally(() => dispatch(pending(false)))
    }

}

export function updateMainData(liveDto) {
    return dispatch => {
        dispatch(pending(true))
        put(edgeAPIs.server(), liveDto).then(res => {
            dispatch(liveData(res))
        }).catch(err => {
            dispatch(error(err))
        }).finally(() => dispatch(pending(false)))
    }

}

export function deleteMainData(id) {
    return dispatch => {
        dispatch(pending(true))
        deleted(edgeAPIs.server(), id).then(res => {
            dispatch(liveData(res))
        }).catch(err => {
            dispatch(error(err))
        }).finally(() => dispatch(pending(false)))
    }

}

export function addNewData(liveDto) {
    return dispatch => {
        dispatch(pending(true))
        post(edgeAPIs.server(), liveDto).then(res => {
            dispatch(liveData(res))
        }).catch(err => {
            dispatch(error(err))
        }).finally(() => dispatch(pending(false)))
    }

}