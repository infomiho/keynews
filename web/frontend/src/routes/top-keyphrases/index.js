import { h, Component } from 'preact';
import { connect } from 'preact-redux';
import style from './style';

import { setLoading } from '../../store/actions';
import { makeCompoundId } from '../../components/Graph/helpers';

import api from '../../api';
@connect(null, { setLoading })
export default class TopKeyphrases extends Component {
	constructor(props) {
		super(props);
		this.state = {
			keywords: []
		};
	}
	componentDidMount() {
		this.props.setLoading(true);
		api.getTopKeywords().then(result => {
			this.setState({ keywords: result.data });
			this.props.setLoading(false);
		});
	}
	render() {
		const { keywords } = this.state;
		return (
			<div class={style.TopKeyPhrases}>
				{keywords.map((keyword, index) => (
					<h1 style={style.TopKeyPhrases.h1}>
						{index + 1}.{' '}
						<a href={`/keyphrase/${makeCompoundId(keyword.id)}`}>
							{keyword.value}
						</a>{' '}
						({keyword.count})
					</h1>
				))}
			</div>
		);
	}
}
