function update_groups() {
    $.ajax({
        url : $("#post-form").attr("data-groups-url"), // ajax url
        data : { gene_col_idx : $('#gene-selector').val() },

        success : function(data) {
            console.log("Updating Sample Columns"); // sanity check
            $("#post-group").html(data);
        },
    });
}

function load_volcano_plot() {
    $.ajax({
        url : $("#post-form").attr("action"),
        data : $("#post-form").serialize(),

        success : function(data) {
            console.log("Loading Graph");
            $("#volcano-plot").html(data).text();
            console.log(data);
        },
    });
}

// Submit post on submit
$('#post-form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!");  // sanity check
    load_volcano_plot();
});

$('#gene-selector').on("change", function () {
    console.log($('#gene-selector').val());
    update_groups();
});
