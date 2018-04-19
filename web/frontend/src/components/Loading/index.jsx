import { h, Component } from 'preact';

import style from './style';

export default class Loading extends Component {
	render() {
		return (
			<div class={style.Loading}>
				<div class="sk-folding-cube">
					<div class="sk-cube1 sk-cube" />
					<div class="sk-cube2 sk-cube" />
					<div class="sk-cube4 sk-cube" />
					<div class="sk-cube3 sk-cube" />
				</div>
			</div>
		);
	}
}
