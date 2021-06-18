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
    on('input[name=value_forfeit]', 'keypress', somenteNumeros);
    on('input[name=value]', 'keypress', somenteNumeros);   
    on('input[name=ref_month]', 'keypress', somenteNumeros);
    on('input[name=number_req_nimbi]', 'keypress', somenteNumeros);
    on('input[name=number_cod_nimbi]', 'keypress', somenteNumeros);    
    on('input[name=number_pc_nimbi]', 'keypress', somenteNumeros);
    on('input[name=number_cod_project]', 'keypress', somenteNumeros);
    on('input[name=number_cost_center]', 'keypress', somenteNumeros);
    
  })(document,window)