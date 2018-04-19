import { createStore } from 'redux';
import moment from 'moment';

let ACTIONS = {
	SET_DATES: (state, { dates }) => ({
		...state,
		dateFrom: dates.dateFrom,
		dateTo: dates.dateTo
	}),
	SET_LOADING: (state, { loading }) => ({
		...state,
		loading
	})
};

const INITIAL = {
	dateFrom: moment().subtract(1, 'day'),
	dateTo: moment(),
	loading: false
};

export default createStore(
	(state, action) =>
		action && ACTIONS[action.type]
			? ACTIONS[action.type](state, action)
			: state,
	INITIAL,
	typeof devToolsExtension === 'function' ? devToolsExtension() : undefined
);
