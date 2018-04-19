import { h, Component } from 'preact';
import cytoscape from 'cytoscape';
import spread from 'cytoscape-spread';
import coseBilkent from 'cytoscape-cose-bilkent';

cytoscape.use(coseBilkent);

const LAYOUT = {
	name: 'cose-bilkent',
	nodeDimensionsIncludeLabels: true,
	numIter: 5000
};

export default class Cytoscape extends Component {
	cyelement = null;
	cy = null;

	componentDidMount() {
		let cy = cytoscape({
			container: this.cyelement,
			style: [
				{
					selector: 'node',
					style: {
						'background-color': 'data(color)',
						label: 'data(title)',
						'font-size': '12px',
						'text-halign': 'center',
						'text-outline-color': 'data(color)',
						'text-outline-width': '2px',
						color: '#333',
						'overlay-padding': '6px',
						'z-index': 10
					}
				},
				{
					selector: 'edge',
					style: {
						width: 3,
						'line-color': 'data(color)',
						'target-arrow-color': 'data(color)',
						'target-arrow-shape': 'triangle'
					}
				},
				{
					selector: 'node.highlight',
					style: {
						'border-color': '#FFF',
						'border-width': '2px'
					}
				},
				{
					selector: 'node.semitransp',
					style: { opacity: '0.35' }
				},
				{
					selector: 'edge.highlight',
					style: { 'mid-target-arrow-color': '#FFF' }
				},
				{
					selector: 'edge.semitransp',
					style: { opacity: '0.2' }
				}
			],
			layout: LAYOUT,
			// userZoomingEnabled: false,
			wheelSensitivity: 0.1	,
			elements: this.props.elements
		});

		this.cy = cy;
	}

	shouldComponentUpdate() {
		return false;
	}

	componentWillReceiveProps(nextProps) {
		this.cy.json(nextProps);
		this.cy.layout(LAYOUT);
	}

	componentWillUnmount() {
		this.cy.destroy();
	}

	getCy() {
		return this.cy;
	}

	render() {
		return <div ref={elem => (this.cyelement = elem)} />;
	}
}
