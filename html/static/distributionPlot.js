function countValuesInBuckets(extents, nBuckets, values) {
	var bucketSize = (extents[1] - extents[0]) / nBuckets;
	var bucketForValue = function(val) {
		var b = Math.floor((val - extents[0]) / bucketSize) * bucketSize;
		if (b == extents[1]) b -= bucketSize;
		return b;
	}
	var counts = {};
	getBuckets(extents, nBuckets).forEach(function(bucket) {
		counts[bucket] = 0;
	})
	values.forEach(function(x) {
		var bucket = bucketForValue(x);
		counts[bucket]++;
	})
	return counts;
}

function convertCountDictToPercentageDict(counts) {
	var total = 0;
	Object.keys(counts).forEach(function(k) {
		total += counts[k];
	});
	var percents = {};
	Object.keys(counts).forEach(function(k) {
		percents[k] = counts[k] / total;
	})
	return percents;
}

function getBuckets(extents, nBuckets) {
	var bucketForValue = function(val) {
		var b = Math.floor((val - extents[0]) / bucketSize) * bucketSize;
		if (b == extents[1]) b -= bucketSize;
		return b;
	}
	var buckets = [];
	var bucketSize = (extents[1] - extents[0]) / nBuckets;
	for (var i=0; i<nBuckets; i++) {
		buckets.push(bucketForValue(extents[0] + bucketSize * (i+0.5) ));
	}
	return buckets;
}

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
	var bucketSize = (extents[1] - extents[0]) / (nBuckets);
	// put the values in the buckets:
	var buckets = getBuckets(extents, nBuckets);
	buckets.sort(function(a,b) {
		return a-b;
	});
	
	var totalBucketPercentages = convertCountDictToPercentageDict(countValuesInBuckets(extents, nBuckets, values));
	
	// create scales:
	var xScale = d3.scale.linear().domain([d3.min(buckets), d3.max(buckets) + bucketSize]).range([0, width]);
	var yScale = d3.scale.linear().domain([0, 1]).range([height, 0]);
	
	// add axes:
	var formatPercent = d3.format(".0%");
	// var xAxis = d3.svg.axis().scale(xScale).ticks(nBuckets);
	var yAxis = d3.svg.axis().scale(yScale).ticks(10).orient("right").tickSize(1).tickFormat(formatPercent);
  /*svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);*/
  svg.append("g")
      .attr("class", "y axis")
      .attr("transform", "translate(" + width + ",0)")
      .call(yAxis);
	
	/*
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
	})*/
			
	// draw labels for the bars:
	svg.selectAll('.bar-label').data(buckets).enter().append('text')
	.attr('class', 'axis')
	.text(function(bucket){ return bucket.toFixed(1) + '–' + (bucket+bucketSize).toFixed(1) })
	.attr('x', function(bucket) {
		return xScale(bucket) + (width / nBuckets - 2) / 2;
	}).attr('text-anchor', 'start').attr('y', function() {return height + 20});
	
	// draw bars separating each bucket:
	svg.selectAll('.bar-separator').data(buckets).enter().append('line').attr('class', 'bar-separator')
	.attr('x2', xScale)
	.attr('x1', xScale)
	.attr('y2', function(){ return 0 })
	.attr('y1', function(){ return height })
	.attr('stroke', '#aaa');
	
	var segments = [totalBucketPercentages];
	var segmentKeys = [];
	if (params.segment) {
		var segmentValues = [];
		var segmentsByKey = {};
		DATA.forEach(function(couple) {
			var value = parseFloat(couple[params.x]);
			if (!isNaN(value)) {
				var segmentKey = couple[params.segment];
				if (segmentKey !== undefined && segmentKey !== 'MISSING') {
					// add this value:
					if (segmentsByKey[segmentKey] === undefined) {
						segmentsByKey[segmentKey] = [];
						segmentValues.push(segmentsByKey[segmentKey]);
						segmentKeys.push(segmentKey);
					}
					segmentsByKey[segmentKey].push(value);
				}
			}
		})
		segments = segmentValues.map(function(values) {
			var counts = countValuesInBuckets(extents, nBuckets, values);
			return convertCountDictToPercentageDict(counts);
		})
	}
	
	var colorLegend = d3.select(div).append('div').attr('class', 'color-legend');
	
	var colors = ['#FE4365', '#83AF9B', '#FC9D9A', '#F9CDAD', '#C8C8A9'];
	for (var i=0; i<segments.length; i++) {
		var bucketPercentages = segments[i];
		var color = colors[i % colors.length];
		
		var START = 'START';
		var END = 'END';
		
		var path = d3.svg.area().x(function(bucket) {
			if (bucket === START) {
				return xScale(extents[0]);
			} else if (bucket === END) {
				return xScale(extents[1]);
			} else {
				return xScale(bucket + bucketSize / 2);
			}
		}).y0(function(bucket) {
			return height;
		}).y1(function(bucket) {
			if (bucket === START || bucket === END) {
				return yScale(0);
			} else {
				return yScale(bucketPercentages[bucket]);
			}
		}).interpolate('cardinal');
		var data = [START].concat(buckets, [END]);
		svg.append('path').datum(data).attr({'class': 'line', 'd': path, 'opacity': 0.5, 'fill': color});
	}
	
	if (params.segment) {
		// create a color legend for each value that we create a segment for:
		var counts = range(0, segments.length);
		d3.select(div).append('div')
		.attr('class', 'color-legend')
		.selectAll('div')
		.data(range(0, segments.length))
		.enter()
		.append('div')
		.text(function(i) {
			var key = segmentKeys[i];
			return (FIELD_VALUE_NAMES[params.segment] || {})[key] || key;
		}).style('background-color', function(i) {
			return colors[i%colors.length];
		});
	}
}
