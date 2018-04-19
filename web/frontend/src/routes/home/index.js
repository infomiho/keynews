import { h, Component } from 'preact';
import { connect } from 'preact-redux';
import { setLoading } from '../../store/actions';
import style from './style';

import Graph from '../../components/Graph';
import { makeElements } from '../../components/Graph/helpers';
import Dates from '../../components/Dates';

import api from '../../api';

const mapStateToProps = state => ({
	dateFrom: state.dateFrom,
	dateTo: state.dateTo
});
@connect(mapStateToProps, { setLoading })
export default class Home extends Component {
	constructor(props) {
		super(props);
		this.state = {
			keywords: []
		};
	}
	setDates = dates => {
		this.setState({
			dateFrom: dates.dateFrom,
			dateTo: dates.dateTo
		});
	};
	componentWillReceiveProps(newProps) {
		if (
			newProps.dateFrom !== this.props.dateFrom ||
			newProps.dateTo !== this.props.dateTo
		) {
			this.load(newProps);
		}
	}
	load = ({ dateFrom, dateTo }) => {
		this.props.setLoading(true);
		api
			.getTrending({ dateFrom, dateTo })
			.then(result => {
				this.setState({ keywords: result.data });
				this.props.setLoading(false);
			})
			.catch(error => {
				this.props.setLoading(false);
				console.error(error);
			});
	};
	componentDidMount() {
		this.load(this.props);
	}
	render() {
		const { keywords } = this.state;
		return (
			<div class={style.home}>
				<h1 class={`title is-2 ${style.MainTitle}`}>
					<div class={style.MainTitle__Title}>Trending key phrases</div>
					<div class={style.Dates}>
						<Dates />
					</div>
				</h1>
				{keywords.length > 0 && <Graph elements={makeElements(keywords)} />}
			</div>
		);
	}
}
