import { actionHandlers } from "./handler"

const initialState = {
    mainData: [],
}

export default function reducer(state = initialState, action) {
    const handle = actionHandlers[action.type]
    return handle ? handle(state, action) : state;
}