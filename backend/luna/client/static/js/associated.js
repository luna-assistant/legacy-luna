
const iniciar = () => {

  formCreateInit();
  $('.modal').modal();
  if ($('.modal').hasClass('error'))
    $('.modal').modal('show');
  $('.button.add').click(openModalCreate);
  
}

const formCreateInit = () => {
  $('form.modal.add').form({
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
}

const openModalCreate = () => {
  $('.modal.add').modal('show');
}

$(iniciar());
