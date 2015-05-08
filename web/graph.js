
(function() {
	var fieldNames = {
		'age_difference': 'Age difference',
		'relationship_quality': 'Self-assessed relationship quality (0 – 4)',
		'respondent_yrsed': "Respondent's years of education",
		'partner_yrsed': "Partner's years of education"
	}
	
	var aggregatePoints = function(points, keyFunc) {
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
	
	var uniqueValues = function(values) {
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
	
	var range = function(from, to) {
		var r = [];
		for (var i=from; i<to; i++) {
			r.push(i);
		}
		return r;
	}
	
	var createGraph = function(div) {
		var params = $(div).data();
		
		var width = params.width || 800;
		var height = params.height || 400;
		var axisLabelHeight = 40;
		var scaleLabelHeight = 20;
		
		var dataRect = {
			x: axisLabelHeight + scaleLabelHeight, 
			y: 0, 
			width: width - (axisLabelHeight + scaleLabelHeight),
			height: height - (axisLabelHeight + scaleLabelHeight)};
		
		var svg = d3.select(div).append("svg")
			.attr('viewBox', '0 0 ' + width + ' ' + height);
		
		// add axis labels:
		var leftAxis = svg.append('text')
			.attr('class', 'left axis')
			.attr('x', axisLabelHeight / 2)
			.attr('y', dataRect.y + dataRect.height/2)
			.attr('transform', 'rotate(-90 ' + (axisLabelHeight / 2) + ' ' + (dataRect.y + dataRect.height/2) + ')')
			.text(fieldNames[params.y]);
		
		var bottomAxis = svg.append('text')
			.attr('class', 'bottom axis')
			.attr('x', dataRect.x + dataRect.width / 2)
			.attr('y', height - axisLabelHeight/2)
			.text(fieldNames[params.x]);
		
		// add axis lines:
		var leftAxisLine = svg.append('line').attr({'class': 'axis', x1: dataRect.x, y1: dataRect.y, x2: dataRect.x, y2: dataRect.y + dataRect.height});
		var rightAxisLine = svg.append('line').attr({'class': 'axis', x1: dataRect.x, y1: dataRect.y + dataRect.height, x2: dataRect.x + dataRect.width, y2: dataRect.y + dataRect.height});
		
		// bind the data:
		d3.csv(params.csv, function(data) {
			var getX = function(d) { return parseFloat(d[params.x]); };
			var getY = function(d) { return parseFloat(d[params.y]); };
			var graphableData = data.filter(function(data) {
				return !isNaN(getX(data)) && !isNaN(getY(data));
			});
			var xs = graphableData.map(getX);
			var ys = graphableData.map(getY);
			
			var aggregated = aggregatePoints(graphableData, function(point) {
				return point[params.x] + ',' + point[params.y];
			});
			var counts = aggregated.map(function(item){ return item.points.length; });
						
			var bounds = function(nums) { return [d3.min(nums), d3.max(nums)] };
			var padding = 20;
			var xScale = d3.scale.linear().domain(bounds(xs)).range([dataRect.x + padding, dataRect.width + dataRect.x - padding]);
			var yScale = d3.scale.linear().domain(bounds(ys)).range([dataRect.y + dataRect.height - padding, dataRect.y + padding]);
			
			var radiusScale = d3.scale.sqrt().domain(bounds(counts)).range([2, 20]);
			
			svg.selectAll('.dot').data(aggregated).enter()
				.append('circle')
				.attr('class', 'dot')
				.attr('r', function(data) { return radiusScale(data.points.length) })
				.attr('cx', function(data) { return xScale(getX(data.points[0])) })
				.attr('cy', function(data) { return yScale(getY(data.points[0])) });
			
			// add scale labels:
			var xLabelCount = Math.min(7, uniqueValues(xs).length);
			var yLabelCount = Math.min(5, uniqueValues(ys).length);
	
			var xLabels = svg.selectAll('.x.scale-label').data(range(0,xLabelCount)).enter().append('text').attr({'class': 'x scale-label', y: dataRect.y + dataRect.height}).text(function(i){
				var value = xScale.copy().range([0, 1]).invert(i / xLabelCount);
				return value.toFixed(2);
			}).attr('x', function(i) {
				var value = xScale.copy().range([0, 1]).invert(i / xLabelCount);
				return Math.round(xScale(value));
			});
			
			var yLabels = svg.selectAll('.y.scale-label').data(range(0,yLabelCount)).enter().append('text').attr({'class': 'y scale-label', x: dataRect.x}).text(function(i){
				var value = yScale.copy().range([0, 1]).invert(i / yLabelCount);
				return value.toFixed(2);
			}).attr('y', function(i) {
				var value = yScale.copy().range([0, 1]).invert(i / yLabelCount);
				return Math.round(yScale(value));
			}).attr('transform', function(i) {
				var value = yScale.copy().range([0, 1]).invert(i / yLabelCount);
				var y = yScale(value);
				var x = dataRect.x;
				return 'rotate(-90 ' + x + ' ' + y + ')';
			});
		});
	}
	
	$(document).ready(function() {
		$(".graph").each(function(i, div) {
			createGraph(div);
		});
	});
})();
