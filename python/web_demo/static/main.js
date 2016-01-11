$(document).ready(function() {

    function displayResult(tokens) {
        var $resultDiv = $("#punctuation");
        $resultDiv.empty("");
        tokens.forEach(function(token) {
            if (token.type == "word") {
                $resultDiv.append("<span class='token token-" + token.type + "'>" + token.token + "</span>");
            } else if (token.type == "punctuation") {
                var probs_str = "";
                for (var key in token.probs) {
                    probs_str += key + ": " + (token.probs[key] * 100 ).toFixed(2) + "% &#013;"
                };
                $resultDiv.append("<span title='" + probs_str + "' class='token token-" + token.punctuation + "'>" + token.punctuation + "</span>");
            }
        });
    };

    $("#button-punctuate").click(function() {
        var text = {
            text: $('#textarea-input').val()
        };
        $.post("/classify", text, function(response, textStatus) {
                displayResult(response);
            }, "json")
        .fail(function(data) {
            console.error(data);
        });
	});

    $("#selection-config").on('change', function() {
        console.log("dkdjslkd")
 
        var setting = {
            folder: $("#selection-config").val()
        };

        $.post("/settings", setting, function(response, textStatus) {
            })
        .fail(function(data) {
            console.error(data);
        });
    });

});
