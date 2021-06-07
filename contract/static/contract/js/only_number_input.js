(function(doc,win){
    'use strict';  
    
    function somenteNumeros(e) {        
        var charCode = e.charCode ? e.charCode : e.keyCode;            
        // charCode 8 = backspace   
        // charCode 9 = tab
        if (charCode != 8 && charCode != 9) {
            // charCode 48 equivale a 0   
            // charCode 57 equivale a 9
            if (charCode < 48 || charCode > 57) {                  
                e.preventDefault();                        
            }
        }
    }  
    function on(element, event, callback){
        doc.querySelector(element).addEventListener(event,callback,false);
    }
    on('input[name=cnpj]', 'keypress', somenteNumeros);
    on('input[name=address_number]', 'keypress', somenteNumeros);
    on('input[name=zip_code]', 'keypress', somenteNumeros);
    on('input[name=phone_1]', 'keypress', somenteNumeros);
    on('input[name=phone_2]', 'keypress', somenteNumeros);
    
  })(document,window)