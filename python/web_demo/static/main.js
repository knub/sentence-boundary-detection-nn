$(document).ready(function() {

    function displayResult(tokens) {
        var $resultDiv = $("#punctuation");
        $resultDiv.empty("");
        tokens.forEach(function(token) {
            if (token.type == "word") {
                var tag_str = "";
                for (var key in token.pos) {
                    tag_str += token.pos[key] + "&#013;"
                };
                $resultDiv.append("<span title='" + tag_str + "' class='token token-" + token.type + "'>" + token.token + "</span>");
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
            text: $('#textarea-input').val(),
            textfile: $('#selection-text-file').val()
        };
        $.post("/classify", text, function(response, textStatus) {
                displayResult(response);
            }, "json")
        .fail(function(data) {
            console.error(data);
        });
	});

    $("#selection-config").on('change', function() {
        var setting = {
            folder: $("#selection-config").val()
        };

        $.post("/settings", setting, function(response) {})
        .fail(function(data) {
            console.error(data);
        });
    });

    function loadConfigOptions() {
        $.get("/settings", function(response) {
            response.options.forEach(function(option){

                if (response.selected === option){
                    $('#selection-config').append($('<option>', {
                         value: option,
                         text: option,
                         selected:"selected"
                    }));
                }
                else{
                    $('#selection-config').append($('<option>', {
                         value: option,
                         text: option
                    })); 
                }
            });
        }, "json")
        .fail(function(data) {
            console.error(data);
        });
    };

    function loadTextFileOptions() {
        $.get("/files", function(response) {
            response.forEach(function(option){
                $('#selection-text-file').append($('<option>', {
                     value: option,
                     text: option,
                }));
            });
        }, "json")
        .fail(function(data) {
            console.error(data);
        });
    };


    loadTextFileOptions();
    loadConfigOptions();

});
