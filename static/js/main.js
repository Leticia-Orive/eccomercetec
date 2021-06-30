$(function(){
    $(".btn-script").click(function(){
        console.log("pulsaste delete");
        if(confirm("ESTAS SEGURO DE ELIMINAR EL PRODUCTO AHORA MISMO?")){
            window.location.href = 'http://localhost:8000' + $(this).attr('custom-href');
        }

    });

});