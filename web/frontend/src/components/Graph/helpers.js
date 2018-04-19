import randomColor from 'randomcolor';

export const makeCompoundId = ids => ids[0];

const makeConnected = (parentId, keyword, color, ignore = { list =[], ignoreEdges = false } = {}) => {
	const elements = [];
	const shouldBeIgnored = ignore.list.indexOf(makeCompoundId(keyword.id)) === -1;
	if (shouldBeIgnored) {
		elements.push({
			data: {
				id: makeCompoundId(keyword.id),
				title: keyword.value,
				color
			},
			style: {
				width: 10,
				height: 10
			}
		});
	}
	elements.push({
		data: {
			id: `${makeCompoundId(keyword.id)}${makeCompoundId(parentId)}`,
			source: makeCompoundId(parentId),
			target: makeCompoundId(keyword.id),
			color
		},
		style: {
			shape: 'rectangle'
		}
	});
	return elements;
};

export function makeElements(keywords) {
	let elements = [];
	// We ignore parents in order to avoid adding them as small nodes
	const ignoreParents = keywords.map(keyword => makeCompoundId(keyword.id));
	const maxCount = keywords.reduce(
		(acc, keyword) => Math.max(acc, keyword.count),
		keywords[0].count
	);
	keywords.forEach((keyword, index) => {
		const color = randomColor({ luminosity: 'light', seed: makeCompoundId(keyword.id) });
		const size = Math.max(
			10,
			(keywords.length - index) * (30 / keywords.length)
		); // Math.max(10, keyword.count/maxCount * 50);
		elements.push({
			data: { id: makeCompoundId(keyword.id), title: keyword.value, color },
			style: {
				width: size,
				height: size
			}
		});
		keyword.connected.forEach(connectedKeyword => {
			elements = elements.concat(
				makeConnected(keyword.id, connectedKeyword, color, { list: ignoreParents })
			);
			if (connectedKeyword.connected) {
				const connectedColor = randomColor({ luminosity: 'light', seed: makeCompoundId(connectedKeyword.id) });
				connectedKeyword.connected.forEach(innerConnectedKeyword => {
					elements = elements.concat(
						makeConnected(
							connectedKeyword.id,
							innerConnectedKeyword,
							connectedColor,
							{ list: ignoreParents, ignoreEdges: true }
						)
					);
				});
			}
		});
	});
	return elements;
}
