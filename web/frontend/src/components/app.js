import { h, Component } from 'preact';
import { Router } from 'preact-router';
import { connect } from 'preact-redux';

import Header from './header';
import Home from '../routes/home';
import Search from '../routes/search';
import Keyphrase from '../routes/keyphrase';
import TopKeyPhrases from '../routes/top-keyphrases';
import ConnectedKeyphrases from '../routes/connected-keyphrases';

import Error from '../routes/error';

import Loading from './Loading';

// import Home from 'async!../routes/home';
// import Profile from 'async!../routes/profile';

const mapStateToProps = state => ({
	loading: state.loading
});

@connect(mapStateToProps)
export default class App extends Component {

	/** Gets fired when the route changes.
	 *	@param {Object} event		"change" event from [preact-router](http://git.io/preact-router)
	 *	@param {string} event.url	The newly routed URL
	 */
	handleRoute = e => {
		this.currentUrl = e.url;
	};

	render() {
		const { loading } = this.props;
		return (
			<div id="app">
				<Header />
				{loading && <Loading />}
				<Router onChange={this.handleRoute}>
					<Home path="/" />
					<Search path="/search" />
					<Keyphrase path="/keyphrase/:id" />
					<ConnectedKeyphrases path="/connected-keyphrases/:id1/:id2" />
					<TopKeyPhrases path="/top-keyphrases" />
					<Error type="404" default />
				</Router>
				<footer class="footer">
					<div class="container">
						<div class="content has-text-centered">
							<p>
								<strong>Keynews</strong> created at <a href="#">FER</a>
							</p>
						</div>
					</div>
				</footer>
			</div>
		);
	}
}
