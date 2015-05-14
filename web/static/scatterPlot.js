function createScatterPlot(div, params) {
	var width = params.width;
	var height = params.height;
	var axisLabelHeight = 40;
	var scaleLabelHeight = 20;
	var data = DATA;
	var fieldNames = FIELD_NAMES;
	
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
}