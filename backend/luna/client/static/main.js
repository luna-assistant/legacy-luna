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
});