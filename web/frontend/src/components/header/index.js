import { h, Component } from 'preact';
import { Link } from 'preact-router/match';

import Logo from '../../assets/key_news_logo.png';

import Search from '../Search';
export default class Header extends Component {
	render() {
		return (
			<header>
				<nav className="navbar is-primary">
					<div className="container">
						<div className="navbar-brand">
							<Link className="navbar-item" href="/">
								<img src={Logo} alt="Key news" width="112" height="28" />
							</Link>
							<div
								class="navbar-burger burger"
								data-target="navbarExampleTransparentExample"
							>
								<span />
								<span />
								<span />
							</div>
						</div>

						<div id="navbarExampleTransparentExample" className="navbar-menu">
							<div className="navbar-start">
								<Search />
							</div>
							<div className="navbar-end">
								{/* <Link
									activeClassName="is-active"
									href="/"
									className="navbar-item"
								>
									Home
								</Link> */}
								<Link
									activeClassName="is-active"
									href="/top-keyphrases"
									className="navbar-item"
								>
									Top Key Phrases
								</Link>
							</div>
						</div>
					</div>
				</nav>
			</header>
		);
	}
}
