import { h, Component } from 'preact';
import { connect } from 'preact-redux';

import { setDates } from '../../store/actions';

import style from './style';

import DatePicker from 'react-datepicker';
import moment from 'moment';

import 'react-datepicker/dist/react-datepicker.css';

const mapStateToProps = state => ({
	dateFrom: state.dateFrom,
	dateTo: state.dateTo
});

@connect(mapStateToProps, { setDates })
export default class Dates extends Component {
	handleChangeStart = value => {
		this.props.setDates({
			dateFrom: value,
			dateTo: this.props.dateTo
		});
	};

	handleChangeEnd = value => {
		this.props.setDates({
			dateFrom: this.props.dateFrom,
			dateTo: value
		});
	};

	render() {
		const { dateFrom, dateTo } = this.props;

		return (
			<div class='Dates'>
				<div class="field is-horizontal">
					<div class="field-body">
						<div class="field">
							<DatePicker
								placeholderText="Date from"
								selected={dateFrom}
								selectsStart
								startDate={dateFrom}
								endDate={dateTo}
								onChange={this.handleChangeStart}
								className="input is-medium"
							/>
						</div>

						<div class="field">
							<DatePicker
								placeholderText="Date to"
								selected={dateTo}
								selectsEnd
								startDate={dateFrom}
								endDate={dateTo}
								onChange={this.handleChangeEnd}
								className="input is-medium"
							/>
						</div>
					</div>
				</div>
			</div>
		);
	}
}
