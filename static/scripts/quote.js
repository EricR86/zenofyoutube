$(function() {
    // To calculate the width of the quote we're going to put a "span"
    // around the text, and then take the width of that element
    // and then remove the span (restore the original html)
    var originalText = $("blockquote").html();
    var tempText = "<span>"+originalText+"</span>";
    $("blockquote").html(tempText);
    var text_width = $("blockquote span").width();
    $("blockquote").html(originalText);

    // Position the block quotes accordingly
    text_width += 256; //add space for the block quotes
    $("#quoteBox").width(text_width);
});
