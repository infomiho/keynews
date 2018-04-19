import { h, Component } from 'preact';
import { connect } from 'preact-redux';
import moment from 'moment';

import { setLoading } from '../../store/actions';

import style from './style';

import Graph from '../../components/Graph';
import { makeElements } from '../../components/Graph/helpers';
import api from '../../api';

import Article from './Article';

function sortByDate(a, b) {
	const first = moment.utc(a['published_on']).valueOf();
	const second = moment.utc(b['published_on']).valueOf();
	// DESC
	if (first < second) return 1;
	if (first > second) return -1;
	return 0;
}

@connect(null, { setLoading })
export default class Keyphrase extends Component {
	constructor(props) {
		super(props);
		this.state = {
			keyphrase: undefined,
			articles: []
		};
	}
	load = id => {
		this.setState({
			keyphrase: undefined
		});
		this.props.setLoading(true);
		api
			.getKeyword(id)
			.then(result => {
				const keyphrase = result.data;
				this.setState({
					keyphrase
				});
				this.props.setLoading(false);
				api
					.getArticlesForKeyowrd(id, keyphrase.connected.map(c => c.id[0]))
					.then(result => {
						const articles = result.data;
						articles.sort(sortByDate);
						this.setState({
							articles
						});
					});
			})
			.catch(error => {
				this.props.setLoading(false);
				console.error(error);
			});
	};
	componentDidMount() {
		const { id } = this.props.matches;
		this.load(id);
	}
	componentWillReceiveProps(newProps) {
		if (newProps.matches.id !== this.props.matches.id) {
			this.load(newProps.matches.id);
		}
	}
	render() {
		const { keyphrase, articles } = this.state;
		const keywordArray = keyphrase
			? keyphrase.connected.concat(keyphrase).map(keyphrase => keyphrase.value)
			: [];

		return (
			<div class={style.keyphrase}>
				{keyphrase && (
					<div>
						<h1 class="title is-2">{keyphrase.value}</h1>

						<div class="columns">
							<div class="column">
								<Graph elements={makeElements([keyphrase])} />
							</div>
							{keyphrase['wikipedia_details'] && (
								<div class="column is-one-quarter">
									<div class="card article-card">
										<div class="card-image">
											<figure
												class='article-image'
												style={{
													'background-image': `url(${
														keyphrase['wikipedia_details'].image
													})`
												}}
											/>
										</div>
										<div class="card-content">
											<div class="media">
												<div class="media-content">
													<p class="title is-4">
														{keyphrase['wikipedia_details'].heading}
													</p>
													<p class="subtitle is-6">Article from Wikipedia</p>
												</div>
											</div>

											<div class="content">
												{keyphrase['wikipedia_details'].summary}
												<br />
												<a href={keyphrase['wikipedia_details'].url}>
													Read more
												</a>
											</div>
										</div>
									</div>
								</div>
							)}
						</div>
						<div class="columns is-multiline">
							{articles.map(article => (
								<Article article={article} highlight={keywordArray} />
							))}
						</div>
					</div>
				)}
			</div>
		);
	}
}
