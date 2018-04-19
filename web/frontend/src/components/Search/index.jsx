import { h, Component } from 'preact';

import style from './style';
import Autosuggest from 'react-autosuggest';
import api from '../../api';

import { route } from 'preact-router';

// When suggestion is clicked, Autosuggest needs to populate the input
// based on the clicked suggestion. Teach Autosuggest how to calculate the
// input value for every given suggestion.
const getSuggestionValue = suggestion => suggestion.value;

// Use your imagination to render suggestions.
const renderSuggestion = suggestion => (
	<div onClick={() => route(`/keyphrase/${ suggestion.id }`)}>
		{suggestion.value}
	</div>
);

export default class Search extends Component {
	constructor() {
		super();
		this.state = {
			value: '',
			suggestions: []
		};
	}

	onChange = (event, { newValue }) => {
		this.setState({
			value: newValue
		});
	};

	// Autosuggest will call this function every time you need to update suggestions.
	// You already implemented this logic above, so just use it.
	onSuggestionsFetchRequested = ({ value }) => {
		api.getSearchSuggestions(value).then(result => {
			this.setState({
				suggestions: result.data
			});
		});
	};

	// Autosuggest will call this function every time you need to clear suggestions.
	onSuggestionsClearRequested = () => {
		this.setState({
			suggestions: []
		});
	};

	onSuggestionSelected = (e, { suggestion, suggestionValue, suggestionIndex, sectionIndex, method }) => {
		route(`/keyphrase/${ suggestion.id }`);
	}

	render() {
		const { value, suggestions } = this.state;

		const inputProps = {
			placeholder: 'Search for the key phrase',
			value,
			onChange: this.onChange,
			onKeyPress: e => {
				if(e.key == 'Enter'){
					console.log('enter press here! ')
				}
			}
		};

		const theme = {
			container: style['react-autosuggest__container'],
			containerOpen: style['react-autosuggest__container--open'],
			input: style['react-autosuggest__input'],
			inputOpen: style['react-autosuggest__input--open'],
			inputFocused: style['react-autosuggest__input--focused'],
			suggestionsContainer: style['react-autosuggest__suggestions-container'],
			suggestionsContainerOpen:
				style['react-autosuggest__suggestions-container--open'],
			suggestionsList: style['react-autosuggest__suggestions-list'],
			suggestion: style['react-autosuggest__suggestion'],
			suggestionFirst: style['react-autosuggest__suggestion--first'],
			suggestionHighlighted:
				style['react-autosuggest__suggestion--highlighted'],
			sectionContainer: style['react-autosuggest__section-container'],
			sectionContainerFirst:
				style['react-autosuggest__section-container--first'],
			sectionTitle: style['react-autosuggest__section-title']
		};

		return (
			<Autosuggest
				theme={theme}
				suggestions={suggestions}
				onSuggestionsFetchRequested={this.onSuggestionsFetchRequested}
				onSuggestionsClearRequested={this.onSuggestionsClearRequested}
				getSuggestionValue={getSuggestionValue}
				renderSuggestion={renderSuggestion}
				inputProps={inputProps}
				onSuggestionSelected={this.onSuggestionSelected}
			/>
		);
	}
}
