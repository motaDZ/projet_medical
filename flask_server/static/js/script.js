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


$('#visualiser').click(function(e){
    console.log('button clicked')
    var reader = new FileReader();
    reader.readAsArrayBuffer(document.getElementById('excel_file').files[0]);
    console.log(reader)
    reader.onload = function(e) {
            var data = new Uint8Array(reader.result);
            var wb = XLSX.read(data,{type:'array'});
            
            var sheetNames = wb.SheetNames;

            for (var i = 0; i < sheetNames.length; ++i) {
                    var htmlstr = XLSX.write(wb,{sheet:sheetNames[i], type:'binary',bookType:'html'});
                    $('#wrapper')[0].innerHTML += htmlstr;
                }
                
                
    }



    
});