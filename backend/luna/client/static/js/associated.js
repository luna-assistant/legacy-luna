
const init = () => {

  initForm('form.modal.add');
  $('.modal').modal();
  if ($('.modal').hasClass('error'))
    $('.modal').modal('show');

  $('.button.add').click(openModalCreate);
  $('.button.show').click(function() { openModalShow(this)});
  $('.button.edit').click(function() { openModalEdit(this)});

}

const initForm = (selectQuery) => {
  $(selectQuery).form({
    fields: {
      name: {
        identifier: 'name',
        rules: [{
          type: 'empty', prompt: 'Por favor, insira o nome'
      }]},
      cpf: {
        identifier: 'cpf',
        rules: [{
          type: 'empty', prompt: 'Por favor, insira o CPF'
        },{
          type: 'length[14]', prompt: 'Seu CPF está incompleto'
      }]},
      birth: {
        identifier: 'birth',
        rules: [{
          type: 'empty', prompt: 'Por favor, insira a Data de Nascimento'
        },{
          type: 'regExp',
          value: /^\d{2}\/\d{2}\/\d{4}$/,
          prompt: 'Por favor, insira uma data válida'
      }]}}
  });

  $('.checkbox').checkbox();
}

const openModalCreate = () => {
  $('.modal.add').modal('show');
}

const openModalShow = (button) => {
  let id = $(button).closest('tr[data-id]').data('id');

  $.ajax({
    url: '/associados/visualizar/' + id,
    success: function(modal) {
      $('.ajax.modals').html('');
      $('.ajax.modals').append(modal);

      $('#modalshow' + id).modal('show');
    }
  });
}

const openModalEdit = (button) => {
  let id = $(button).closest('tr[data-id]').data('id');

  $.ajax({
    url: '/associados/editar/' + id,
    success: function(modal) {
      $('.ajax.modals').html('');
      $('.ajax.modals').append(modal);

      $('#modaledit' + id).modal('show');

      $('[data-mask]').map(function(index, element){
        $(element).mask($(element).attr('data-mask'));
      });
      initForm('form.modal.edit');
    }
  });
}

$(init());
