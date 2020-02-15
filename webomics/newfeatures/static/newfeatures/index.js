 function filter_experiments() {
    $.ajax({
        url : $("#filter-form").attr("action"),
        data : $("#filter-form").serialize(),

        success : function(data) {
            console.log("Fetching New Experiments");
            $("#filtered-data").html(data).text();
            console.log(data);
        },
    });
}

// Submit post on submit
$('.form-filter').on('change', function(event){
    console.log("change");  // sanity check
    console.log($('#filter-form').serialize());
    filter_experiments();
});
