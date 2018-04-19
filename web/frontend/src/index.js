import './style';
import App from './components/app';
import store from './store';

import { Provider } from 'preact-redux';

export default () => (
	<div id="outer">
		<Provider store={store}>
			<App />
		</Provider>
	</div>
);
