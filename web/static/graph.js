$(document).ready(function() {
	$(".graph").each(function(i, div) {
		createGraph(div);
	});
});

function createGraph(div) {
	var params = $(div).data();
	params.width = params.width || 800;
	params.height = params.height || 400;
	var type = getGraphType(div);
	var plots = {
		scatter: createScatterPlot, 
		distribution: createDistributionPlot
	};
	plots[type](div, params);
}

// HELPER FUNCTIONS:

function aggregatePoints(points, keyFunc) {
	// takes an array of data points, computes keys using keyFuncs;
	// for each unique key, returns {key: <key>, points: [points]}
	var items = [];
	var itemsByKey = {};
	points.forEach(function(point) {
		var key = keyFunc(point);
		if (itemsByKey[key] === undefined) {
			itemsByKey[key] = {key: key, points: []};
			items.push(itemsByKey[key]);
		}
		itemsByKey[key].points.push(point);
	});
	return items;
}

function uniqueValues(values) {
	var uniques = [];
	var seen = {};
	values.forEach(function(val) {
		if (seen[val] === undefined) {
			uniques.push(val);
			seen[val] = true;
		}
	})
	return uniques;
}

function range(from, to) {
	var r = [];
	for (var i=from; i<to; i++) {
		r.push(i);
	}
	return r;
}

function getGraphType(div) {
	var theType = 'scatter';
	['scatter', 'distribution'].forEach(function(type) {
		if (div.classList.contains(type)) {
			theType = type;
		}
	})
	return theType;
}
