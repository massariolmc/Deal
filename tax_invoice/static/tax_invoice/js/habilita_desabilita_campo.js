(function(doc,win){
    'use strict';  
    var field_1 = doc.querySelector('#id_value_forfeit')  
    var field_2 = doc.querySelector('#id_forfeit_status')  
    
    if (field_2.value === 'Yes'){
        field_1.readOnly = false
    }
    else{
        field_1.readOnly = true
    }
    
    function habilita_desabilita(e) {                
        var check = e.target.value
        if (check === 'Yes'){
            field_1.readOnly = false            
        }
        else{
            field_1.readOnly = true
            field_1.value = "0,00"
        }
    }  
    function on(element, event, callback){
        doc.querySelector(element).addEventListener(event,callback,false);
    }
    on('select[name=forfeit_status]', 'change', habilita_desabilita);    
    
  })(document,window)