var timeline;

google.load("visualization", "1");

// Set callback to run when API is loaded
google.setOnLoadCallback(drawVisualization);

// Called when the Visualization API is loaded.

function drawVisualization() {
    // Create and populate a data table.
    var data = new google.visualization.DataTable();
    data.addColumn('datetime', 'start');
    data.addColumn('datetime', 'end');
    data.addColumn('string', 'content');
    data.addColumn('string', 'group');

    var rows = JSON.parse($("#timeline-data").html());
    for (var i = 0; i < rows.rows.length; i++) {
        var sin_row = rows.rows[i];
        switch (sin_row.length) {
            case 3:
                sin_row = [new Date(sin_row[0]), , sin_row[1], sin_row[2]];
                break;
            case 4:
                sin_row[0] = new Date(sin_row[0]);
                sin_row[1] = new Date(sin_row[1]);
                break;
        }
        sin_row[3] = $("<div/>", {
            "html": $("<span/>", {
                "class": "badge badge-success",
                "html": sin_row[3]
            })
        }).html();
        rows.rows[i] = sin_row;
    };
    data.addRows(rows.rows);

    // specify options
    var options = {
        width: "100%",
        height: "300px",
        style: "box",
        zoomMin: 1000 * 60 * 60 * 24 * 3,
        groupsChangeable: true,
        groupsOnRight: true
    };


    // Instantiate our timeline object.
    timeline = new links.Timeline(document.getElementById('mytimeline'));
    timeline.setOptions({
        locale: "cn"
    });

    // Draw our timeline with the created data and options
    timeline.draw(data, options);
}