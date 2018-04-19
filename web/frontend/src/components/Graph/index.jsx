import { h, Component } from 'preact';
import { route } from 'preact-router';

import Cytoscape from './Cytoscape';

export default class Graph extends Component {
	graph = null;
	componentDidMount() {
		const cy = this.graph.getCy();
		cy.$('node').on('click', e => {
			route(`/keyphrase/${e.target.id()}`);
		});
		cy.$('edge').on('click', e => {
			const ele = e.target;
			route(
				`/connected-keyphrases/${ele.source().id()}/${ele.target().id()}`
			);
		});

		cy.on('mouseover', 'node', e => {
			let sel = e.target;
			cy
				.elements()
				.difference(sel.outgoers())
				.difference(sel.incomers())
				.not(sel)
				.addClass('semitransp');
			sel
				.addClass('highlight')
				.outgoers()
				.incomers()
				.addClass('highlight');
		});
		cy.on('mouseout', 'node', e => {
			let sel = e.target;
			cy.elements().removeClass('semitransp');
			sel
				.removeClass('highlight')
				.outgoers()
				.incomers()
				.removeClass('highlight');
		});
	}
	render() {
		const { elements } = this.props;
		return (
			<div className="Graph">
				<Cytoscape ref={graph => (this.graph = graph)} elements={elements} />
			</div>
		);
	}
}
