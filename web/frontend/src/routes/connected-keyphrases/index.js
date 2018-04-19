import { h, Component } from 'preact';
import { connect } from 'preact-redux';
import style from './style';

import { setLoading } from '../../store/actions';
import Article from '../keyphrase/Article';

import api from '../../api';
@connect(null, { setLoading })
export default class ConnectedKeyphrases extends Component {
	constructor(props) {
		super(props);
		this.state = {
			articles: [],
			keywords: []
		};
	}
	componentDidMount() {
		const { id1, id2 } = this.props.matches;
		this.props.setLoading(true);
		Promise.all([
			api.getKeyword(id1),
			api.getKeyword(id2),
			api.getArticlesForKeyowrd(id1, [id2])
		]).then(results => {
			this.setState({
				keywords: [results[0].data, results[1].data],
				articles: results[2].data
			});
			this.props.setLoading(false);
		});
	}
	render() {
		const { articles, keywords } = this.state;
		return (
			<div class={style.ConnectedKeyphrases}>
				{keywords.length && (
					<h1 class="title is-2">
						{keywords[0].value} + {keywords[1].value}
					</h1>
				)}
				<div class="columns is-multiline">
					{articles.map(article => (
						<Article article={article} highlight={[]} />
					))}
				</div>
			</div>
		);
	}
}
