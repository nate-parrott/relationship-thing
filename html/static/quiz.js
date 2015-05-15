$(document).ready(function() {
	// create the quiz:
	var questions = [
		{name: 'same_sex', prompt: 'Are you a same-sex couple?'},
		{name: 'same_race', prompt: 'Are you and your partner the same race?'},
		{name: 'parental_approval', prompt: 'Do either of your parents approve of the relationship?'},
		{name: 'same_pol', prompt: 'Do you and your partner have the same political affiliation?'},
		{name: 'internet', prompt: 'Did you meet on the Internet?'},
		{name: 'same_religion', prompt: 'Do you and your partner share the same religious or non-religious views?'},
		{name: 'age_gap', prompt: "What's the difference between you and your partner's ages?", type: 'number'}
	]
	questions.forEach(function(q) {
		var div = $("<div></div>").addClass('question').appendTo('#quiz');
		$("<p></p>").text(q.prompt).appendTo(div);
		var inputType = q.type || 'boolean';
		var input = $("<input/>").val('').attr('name', q.name).appendTo(div);
		if (inputType == 'boolean') {
			input.attr('type', 'hidden');
			var options = $("<div></div>").addClass('options').appendTo(div);
			var values = {Yes: '1', No: '0', 'No answer': ''};
			['Yes', 'No', 'No answer'].forEach(function(option) {
				var value = values[option];
				$("<button></button>").text(option).appendTo(options).click(function(e) {
					e.preventDefault();
					$(options).children().removeClass('selected');
					$(e.target).addClass('selected');
					input.val(value);
				});
			});
		} else if (inputType == 'number') {
			input.attr('type', 'number');
		}
	})
	var submit = $("<input type='submit'/>").val("Find out").appendTo($("<div></dov>").appendTo('#quiz'));
})
