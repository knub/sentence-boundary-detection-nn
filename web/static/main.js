$(document).ready(function() {

    function displayResult(tokens) {
        var $resultDiv = $("#punctuation");
        $resultDiv.empty("");
        tokens.forEach(function(token) {
            if (token.type == "word") {
                $resultDiv.append("<span class='token token-" + token.type + "'>" + token.token + "</span>");
            } else if (token.type == "punctuation") {
                $resultDiv.append("<span class='token token-" + token.type + "'>" + token.punctuation + "</span>");
            }
        });
    };

    $("#button-punctuate").click(function() {
        var text = {
            text: $('#textarea-input').val();
        };
        $.post("/classify", text, function(response, textStatus) {
                displayResult(response);
            }, "json")
        .fail(function(data) {
            console.error(data);
        });
	});
});
