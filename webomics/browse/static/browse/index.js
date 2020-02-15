 function filter_experiments() {
    $.ajax({
        url : $("#filter-form").attr("action"),
        data : $("#filter-form").serialize(),

        success : function(data) {
            console.log("succes");
            $("#filtered-data").html(data).text();
        },
    });
}

// Submit post on submit
$('.form-filter').on('change', function(event){
    console.log("change");  // sanity check
    filter_experiments();
});
