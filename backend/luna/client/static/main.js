// custom javascript

$(document).ready(function() {
  $('.ui.dropdown').dropdown();
  $('.ui.checkbox').checkbox();
  
  $('.message .close').on('click', function() {
    $(this).closest('.message').transition('fade');
  });

  let ninthDigit = function(val) {
      return val.replace(/\D/g, '').length === 11
        ? '(00) 00000-0000'
        : '(00) 0000-00009';
    },
    ninthDigitOptions = {
      onKeyPress: function(val, e, field, options) {
        field.mask(ninthDigit.apply({}, arguments), options);
      }
    };

  $('.contact.mask').mask(ninthDigit, ninthDigitOptions);
  
  $('.help.button').click(function() {
    $('#helpModal').modal('show');
  });
  
  $('[data-target=editPasswordForm]').click(function (e) {
    $('#editPasswordForm').modal('show');
  });
  
  $('#editPasswordForm').form({
    fields: {
      old_password: {
        rules: [{
            type: 'empty',
            prompt: 'Por favor, insira sua senha'
          },
          {
            type: 'length[6]',
            prompt: 'Sua senha deve ter no mínimo 6 caracteres'
          }
        ]
      },
      password: {
        rules: [{
            type: 'empty',
            prompt: 'Por favor, insira sua senha'
          },
          {
            type: 'length[6]',
            prompt: 'Sua senha deve ter no mínimo 6 caracteres'
          }
        ]
      },
      confirm: {
        rules: [{
            type: 'empty',
            prompt: 'Por favor, insira a confirmação da senha'
          },{
            type: 'match[password]',
            prompt: 'A confirmação deve ser igual a nova senha informada'
          }
        ]
      }
    }, 
    inline: true,
    on: 'blur'
  })
});