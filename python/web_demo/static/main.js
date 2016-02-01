$(document).ready(function() {

    function displayLexicalAudioResult(tokens) {
        var $resultDivLexicalAudio = $("#punctuation_lexical_audio");
        var $resultDivLexical = $("#punctuation_lexical");
        var $resultDivAudio = $("#punctuation_audio");

        $resultDivLexicalAudio.empty("");
        $resultDivLexical.empty("");
        $resultDivAudio.empty("");

        tokens.forEach(function(token) {
            if (token.type == "word") {
                var tag_str = "";
                for (var key in token.pos) {
                    tag_str += token.pos[key] + "&#013;"
                };
                var s = "<span title='" + tag_str + "' class='token token-" + token.type + "'>" + token.token + "</span>";
                $resultDivLexicalAudio.append(s);
                $resultDivLexical.append(s);
                $resultDivAudio.append(s);
            } else if (token.type == "punctuation") {
                // FUSION
                var probs_str = "";
                for (var key in token.fusion.probs) {
                    probs_str += key + ": " + (token.fusion.probs[key] * 100 ).toFixed(2) + "% &#013;"
                };
                $resultDivLexicalAudio.append("<span title='" + probs_str + "' class='token token-"
                                  + token.fusion.punctuation + "'>" + token.fusion.punctuation + "</span>");
                // LEXICAL
                var probs_str = "";
                for (var key in token.lexical.probs) {
                    probs_str += key + ": " + (token.lexical.probs[key] * 100 ).toFixed(2) + "% &#013;"
                };
                $resultDivLexical.append("<span title='" + probs_str + "' class='token token-"
                                              + token.lexical.punctuation + "'>" + token.lexical.punctuation + "</span>");
                // AUDIO
                var probs_str = "";
                for (var key in token.audio.probs) {
                    probs_str += key + ": " + (token.audio.probs[key] * 100 ).toFixed(2) + "% &#013;"
                };
                $resultDivAudio.append("<span title='" + probs_str + "' class='token token-"
                                              + token.audio.punctuation + "'>" + token.audio.punctuation + "</span>");

            }
        });
    };

    function displayLexicalResult(tokens) {
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


    $("#collapse2").on('hidden.bs.collapse', function () {
        console.log("reached");
        $('#selection-text-file option:contains(---)').prop({selected: true});
    });

    $("#punctuate-lexical").click(function() {
        var text = {
            text: $('#textarea-input').val(),
            textfile: $('#selection-text-file').val(),
            lexical_folder: $("#selection-lexical-models").val()
        };
        $.post("/classify_lexical", text, function(response, textStatus) {
                displayLexicalResult(response);
            }, "json")
        .fail(function(data) {
            console.error(data);
        });
	});

    $("#punctuate-audio-lexical").click(function() {
        var setting = {
            example: $('#selection-audio-examples').val(),
            lexical_folder: $("#selection-lexical-models").val(),
            audio_folder: $("#selection-audio-models").val()
        };
        $.post("/classify_audio_lexical", setting, function(response, textStatus) {
            displayLexicalAudioResult(response);
        }, "json")
            .fail(function(data) {
                      console.error(data);
                  });
    });

    $("#selection-lexical-models").on('change', function() {
        var setting = {
            folder: $("#selection-lexical-models").val()
        };

        $.post("/lexical_models", setting, function(response) {})
        .fail(function(data) {
            console.error(data);
        });
    });

    $("#selection-audio-models").on('change', function() {
        var setting = {
            folder: $("#selection-audio-models").val()
        };

        $.post("/audio_models", setting, function(response) {})
            .fail(function(data) {
                      console.error(data);
                  });
    });

    function loadLexicalModels() {
        $.get("/lexical_models", function(response) {
            response.options.forEach(function(option){

                if (response.selected === option){
                    $('#selection-lexical-models').append($('<option>', {
                         value: option,
                         text: option,
                         selected:"selected"
                    }));
                }
                else{
                    $('#selection-lexical-models').append($('<option>', {
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

    function loadTextFiles() {
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

    function loadAudioExamples() {
        $.get("/examples", function(response) {
            response.forEach(function(option){
                $('#selection-audio-examples').append($('<option>', {
                    value: option,
                    text: option,
                }));
            });
        }, "json")
            .fail(function(data) {
                      console.error(data);
                  });
    };

    function loadAudioModels() {
        $.get("/audio_models", function(response) {
            response.options.forEach(function(option){

                if (response.selected === option){
                    $('#selection-audio-models').append($('<option>', {
                        value: option,
                        text: option,
                        selected:"selected"
                    }));
                }
                else{
                    $('#selection-audio-models').append($('<option>', {
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


    loadTextFiles();
    loadAudioExamples();
    loadLexicalModels();
    loadAudioModels();

});
