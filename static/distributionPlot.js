function createDistributionPlot(div, params) {
	var margin = 80;
	var width = params.width;
	var height = params.height;
	
	var svg = d3.select(div).append("svg")
	.attr('viewBox', '0 0 ' + (width + margin*2) + ' ' + (height + margin*2))
	.append("g")
	.attr("transform", "translate(" + margin + "," + margin + ")");
	
	var values = DATA.map(function(pt) {
		return parseFloat(pt[params.x]);
	}).filter(function(x) {
		return !isNaN(x);
	});
	// create finite # of buckets to hold the values:
	var extents = d3.extent(values);
	var nBuckets = params.buckets || 10;
	var bucketSize = (extents[1] - extents[0]) / (nBuckets - 1);
	var bucketForValue = function(val) {
		return Math.floor((val - extents[0]) / bucketSize) * bucketSize;
	}
	// put the values in the buckets:
	var buckets = [];
	var bucketCounts = {};
	values.forEach(function(x) {
		var bucket = bucketForValue(x);
		if (bucketCounts[bucket] === undefined) {
			bucketCounts[bucket] = 0;
			buckets.push(bucket);
		}
		bucketCounts[bucket]++;
	})
	buckets.sort(function(a,b) {
		return a-b;
	})
	
	// create scales:
	var xScale = d3.scale.linear().domain([d3.min(buckets), d3.max(buckets) + bucketSize]).range([0, width]);
	var yScale = d3.scale.linear().domain(d3.extent(buckets.map(function(bucket) {
		return bucketCounts[bucket];
	}))).range([height, 0]);
	
	// add axes:
	// var xAxis = d3.svg.axis().scale(xScale).ticks(nBuckets);
	var yAxis = d3.svg.axis().scale(yScale).ticks(10).orient("right").tickSize(1);
  /*svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);*/
  svg.append("g")
      .attr("class", "y axis")
      .attr("transform", "translate(" + width + ",0)")
      .call(yAxis);
	
	// draw bars for each bucket:
	svg.selectAll('.bar').data(buckets).enter().append('rect')
	.attr('x', function(bucket) {
		return xScale(bucket);
	}).attr('width', function(bucket) {
		return width / nBuckets - 2;
	}).attr('y', function(bucket) {
		return yScale(bucketCounts[bucket]);
	}).attr('height', function(bucket) {
		return height - yScale(bucketCounts[bucket]); 
	})
	// draw labels for the bars:
	svg.selectAll('.bar-label').data(buckets).enter().append('text')
	.attr('class', 'axis')
	.text(function(bucket){ return bucket })
	.attr('x', function(bucket) {
		return xScale(bucket) + (width / nBuckets - 2) / 2;
	}).attr('text-anchor', 'middle').attr('y', function() {return height + 20});
	
	
	/*var path = d3.svg.area().x(function(bucket) {
		return xScale(bucket);
	}).y0(function(bucket) {
		return height;
	}).y1(function(bucket) {
		return yScale(bucketCounts[bucket]);
	}).interpolate('cardinal');
	svg.selectAll('.line').data([buckets]).enter().append('path').attr({'class': 'line', 'd': path});*/
}
