$(document).ready(function(){ 
    'use strict';   
    //$('.cep').mask('00000-000');    
    //$('.cnpj').mask('00.000.000/0000-00');  
    $('.money').mask('000.000.000.000.000,00', {reverse: true}); 
    $('.ref').mask("00/0000" );     

});

