/*$(function() {
    $('#btn_file_load').click(function() {
 
        $.ajax({
            url: '/excel_upload',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});*/

function to_json(workbook) {
    var result = {};
    workbook.SheetNames.forEach(function(sheetName) {
        var roa = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[sheetName]);
        if(roa.length > 0){
            result[sheetName] = roa;
        }
    });
    return result;
}

function print_sheet(json, sheet) {
    var table = "<br /><b>Feuille: " + sheet + "</b><br /><br /> \
                <table class='table table-bordered'> \
                    <thead>"

    c = 0; 
    loop1:
    for(var j in json[sheet]){
        c++;
        loop2:
        for(var k in json[sheet][j]){
            if (c == 2) break loop1;
            table += "<th>" + k + "</th>"
        }
    }

    table += "</thead> \
              <tbody>"

    c = 0; 
    loop1:
    for(var j in json[sheet]){
        loop2:
        c++;
        table += "<tr>"
        for(var k in json[sheet][j]){
            if (c == 11) break loop1;
            table += "<td>" + json[sheet][j][k] + "</td>"
        }
        table += "</tr>"
    }

    table += "</tbody> \
            </table>"
    
    document.getElementById('sheets').innerHTML = table
}

$('#visualiser').click(function(e){
    var reader = new FileReader();
    reader.readAsArrayBuffer(document.getElementById('excel_file').files[0]);
    reader.onload = function(e) {
            var data = new Uint8Array(reader.result);
            var wb = XLSX.read(data,{type:'array'});

            json = to_json(wb) 



            var buttons = document.createElement('div');
                buttons.setAttribute("id", "buttons");
                buttons.style.padding = "5px";
            var sheets = document.createElement('div');
                sheets.setAttribute("id", "sheets");
                sheets.style.overflowX = "scroll";
            $('#wrapper')[0].appendChild(buttons);
            $('#wrapper')[0].appendChild(sheets);

            for (let sheet in json){
                var button = document.createElement('button');
                    button.className = "btn btn-primary";
                    button.style.marginRight = "5px";
                    button.innerHTML = sheet;
                    button.onclick = function(){
                        print_sheet(json, sheet);
                      };
                document.getElementById('buttons').appendChild(button);
            }

            //$('#wrapper')[0].innerHTML += sheetNames
    }

});