$(document).ready(function () {
    $("#formEstadoObservacion").hide();

    $('#estadoObservacionModal').on('show.bs.modal', function (e) {
        $("#formEstadoObservacion").hide();
        var solicitud_id = $(e.relatedTarget).data('pk');
        $(".solicitud_id").val(solicitud_id);
        var estado = $(e.relatedTarget).data('estado');
        var estado_main = $(e.relatedTarget).data('estado-main');
        var group = $(e.relatedTarget).data('group');

        if (group === 1 && estado === 1) {
            $("#formEstadoObservacion").show();
        }


        if ((group > 1) && (estado === 2 || estado === 0)) {
            $("#formEstadoObservacion").show();
        }

        if (estado_main === 4) {
            $("#formEstadoObservacion").hide();
        }

        estado_form_show(solicitud_id);
    });


    var estado_form_show = (solicitud_id) => {

        $.ajax({
            url: "/solicitud/lista-estados-solicitud",
            data: {
                solicitud_id: solicitud_id
            },
            success: function (data) {
                $("#conent-estado-observado").html(data);
            },
            error: function (request, status, error) {
                alert(request.responseText);
            }
        });
    }

});