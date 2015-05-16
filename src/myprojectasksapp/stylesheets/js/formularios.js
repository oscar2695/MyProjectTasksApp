/**
 * Created by Oscar on 10/04/2015.
 */
function addProject(){
    var tabla = document.getElementById( "Contenedor" );
    var html = '<form id="frmRegister" action="/addproject" method="post" data-fv-framework="bootstrap" data-fv-message="This value is not valid" data-fv-feedbackicons-valid="glyphicon glyphicon-ok" data-fv-feedbackicons-invalid="glyphicon glyphicon-remove" data-fv-feedbackicons-validating="glyphicon glyphicon-refresh">' +
        '               <div class="form-group">' +
        '                   <label for="project" style="color: #ffffff">Nombre</label>' +
        '                   <input type="text" class="form-control" id="project" name="project" placeholder="Nombre del Proyecto" required data-fv-notempty-message="The username is required and cannot be empty">' +
        '               </div>' +
        '               <button type="submit" class="btn btn-default">Registrar</button>' +
        '        </form>'
    tabla.innerHTML= html;
}

function addTask(project){
    var tabla = document.getElementById( "Contenedor" );
    //var cadena= $.url.attr('pro');
    var html = '<form id="frmRegister" action="/addtask?pro='+project+'" method="post">' +
        '               <div class="form-group">' +
        '                   <label for="name" style="color: #ffffff">Nombre</label>' +
        '                   <input type="text" class="form-control" id="name" name="name" placeholder="Nombre " required>' +
        '               </div>' +
        '               <div class="form-group">' +
        '                   <label for="description" style="color: #ffffff">Descripcion</label>' +
        '                   <textarea  type="text" class="form-control" id="description" name="description" placeholder="Descripcion"></textarea>' +
        '               </div>' +
        '               <div class="form-group">' +
        '                   <label for="duration" style="color: #ffffff">Duracion en minutos</label>' +
        '                   <input type="number" min="0" class="form-control bfh-number" id="duration" name="duration" placeholder="Duracion" required data-fv-integer="true" data-fv-integer-message="The value is not an integer">' +
        '               </div>' +
        '               <button type="submit" class="btn btn-default">Registrar</button>' +
        '        </form>';

        tabla.innerHTML= html;
}
