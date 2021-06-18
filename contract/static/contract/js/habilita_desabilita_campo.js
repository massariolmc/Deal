(function(doc,win){
    'use strict';  
    var field_1 = doc.querySelector('#id_dt_conclusion')  
    var field_2 = doc.querySelector('#id_status')  
    
    if (field_2.value === 'Encerrado'){
        //field_1.readOnly = false
        field_1.disabled = false
    }
    else{
        //field_1.readOnly = true
        field_1.disabled = true
    }
    
    function habilita_desabilita(e) {                
        var check = e.target.value
        if (check === 'Encerrado'){
            //field_1.readOnly = false            
            field_1.disabled = false            
        }
        else{
            //field_1.readOnly = true
            field_1.disabled = true
            field_1.value = ""
        }
    }  
    function on(element, event, callback){
        doc.querySelector(element).addEventListener(event,callback,false);
    }
    on('select[name=status]', 'change', habilita_desabilita);    
    
  })(document,window)