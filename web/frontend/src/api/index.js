import axios from 'axios';
import moment from 'moment';

const url = path => {
	const root =
		process.env.NODE_ENV === 'development' ? 'http://localhost:5000' : '';
	return `${root}${path}`;
};

const get = path => axios.get(url(path));
const post = (path, data) => axios.post(url(path), data);

export default {
	getTrending({ dateFrom, dateTo }) {
		let query = '';
		if (dateFrom !== null && dateTo !== null) {
			query = `?date_start=${ dateFrom.format('YYYY-MM-DD') }&date_end=${ dateTo.format('YYYY-MM-DD') }`
		}
		return get(`/trending${ query }`);
	},
	getTopKeywords() {
		return get('/top-keywords');
	},
	getKeyword(id) {
		return get(`/keywords/${id}`);
	},
	getSearchSuggestions(search) {
		return get(`/search?search=${search}`);
	},
	getArticlesForKeyowrd (id, connected) {
		return post('/articles_connected', { id, connected });
	},
	// getArticlesForKeywords (id1, id2) {
	// 	return get(`/articles_keyword/${ id1 }/${ id2 }`)
	// }
};
