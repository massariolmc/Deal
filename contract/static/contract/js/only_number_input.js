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
    
    if ( $( "#id_number_req_nimbi" ).length ) { //valida se elemento existe
        on('input[id=id_number_req_nimbi]', 'keypress', somenteNumeros);
        on('input[id=id_number_cod_nimbi]', 'keypress', somenteNumeros);    
        on('input[id=id_number_pc_nimbi]', 'keypress', somenteNumeros);
        on('input[id=id_number_cod_project]', 'keypress', somenteNumeros);
        on('input[id=id_number_cost_center]', 'keypress', somenteNumeros);
    }
    
    if ( $( "#id_number_months" ).length ) { 
        on('input[name=number_months]', 'keypress', somenteNumeros);
    }

    
    
  })(document,window)