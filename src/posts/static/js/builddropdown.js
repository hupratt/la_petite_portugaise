buildDropdown = () => {
    // build from flagstrap.min.js loaded earlier
    $(".flagstrap").flagStrap();
    // select client's browser language and store it in the meta
    var lang = $("meta")
        .first()
        .attr("ref");
    if (lang == "en") {
        flag = "gb";
    } else {
        flag = lang;
    }
    // add the client's browser language as icon as default 
    const query =
        '<i class="flagstrap-icon flagstrap-' +
        flag +
        '" style="margin-right: 10px;margin-bottom: 2px;margin-left:12px;"></i>';
    $(".dropdown-toggle")
        .children()
        .first()
        .append(query);
    // for some reason the href tags don't work so need to add this piece of code
    $(".dropdown-link").click(function () {
        window.location = $(this).attr("href");
    });
}