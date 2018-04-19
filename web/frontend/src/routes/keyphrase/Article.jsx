import { h, Component } from 'preact';

import style from './style';

const highlightKeywords = (summary, highlight) => {
	highlight.forEach(what => {
		const pattern = new RegExp('(' + what + ')', 'g');
		summary = summary.replace(pattern, '<mark>$1</mark>');
	});
	return summary;
};

export default class Article extends Component {
	render() {
		const { article, highlight } = this.props;
		return (
			<div class="column is-one-quarter">
				<div class="card article-card">
					<div class="card-image">
						<figure
							class='article-image'
							style={{
								'background-image': `url(${article.photo})`
							}}
						/>
					</div>
					<div class="card-content">
						<div class="content">
							<h1 class="title is-4">
								<a href={article.link}>
									{article.title}
								</a>{' '}
								{article.keywords.map(keyword => (
									<span>
										{' '}
										<span class="tag is-light is-medium">{keyword}</span>
									</span>
								))}
							</h1>
							<div
								dangerouslySetInnerHTML={{
									__html: highlightKeywords(article.summary, highlight)
								}}
							/>
							<br />
							<a href={article.link}>Read more</a>
						</div>
					</div>
				</div>
			</div>
		);
	}
}
