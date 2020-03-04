//Need two update calls
function update_groups() {
    $.ajax({
        url : $("#volcano-form").attr("data-groups-url"), // ajax url
        data : { gene_col_idx : $('#gene-selector').val()},

        success : function(data) {
            console.log("Updating Sample Columns"); // sanity check
            $("#volcano-group").html(data.groups);
            $("#pca-group").html(data.pca);
        },
    });
}

function load_volcano_plot() {
    $.ajax({
        url : $("#volcano-form").attr("volcano-url"),
        data : $("#volcano-form").serialize(),

        success : function(data) {
            console.log("Loading Volcano");
            $("#volcano-plot").html(data).text();
        },
    });
}

function load_pca_plot() {
    $.ajax({
        url : $("#pca-form").attr("pca-url"),
        data : $('#pca-form').serialize(),

        success : function(data) {
            console.log("Loading PCA");
            $("#pca-plot").html(data).text();
        },
    });
}

// Submit post on submit
$('#volcano-form').on('submit', function(event){
    event.preventDefault();
    console.log("volcano form submitted!");  // sanity check
    load_volcano_plot();
});

$('#pca-form').on('submit', function(event) {
    event.preventDefault();
    console.log("pca form submitted!");
    load_pca_plot();
});

$('#gene-selector').on("change", function () {
    console.log($('#gene-selector').val());
    $('#gene-copy').val($(this).val());
    update_groups();
});

$(document).ready(function() {
    $('#gene-copy').val($('#gene-selector').val());
});
