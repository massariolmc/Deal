(function(doc,win){
    doc.addEventListener("DOMContentLoaded", function() {
        'use strict';                
        var $click_checkbox = doc.querySelector('[data-js="click_checkbox"]');               
        var $modal_link = doc.querySelector('[data-js="modal_link_delete"]');               
        var $form_modal = doc.querySelector('[name="form_modal_delete_all"]');
        var $form_modal_hidden_values_checkbox = doc.querySelector('[data-js="hidden_values_checkbox"]');
        
        function handleClickDelete(){
            var elementoAtual = doc.querySelectorAll('[data-js="link_delete"');
            Array.prototype.slice.call(elementoAtual).forEach(function(pegaElementoAtual){
                pegaElementoAtual.addEventListener('click', function(e){
                        e.preventDefault();                             
                        $modal_link.setAttribute('action',e.target.getAttribute('data-url'));
                        $('[data-js="modal_delete"]').modal();
                });                             
            }); 
        }   

        function on(element, event, callback){
            doc.querySelector(element).addEventListener(event,callback,false);
        }
        
        function getCheckBox(checkbox){
            var ac = [];
            for (var i=0; i < checkbox.length; i++){
                if(checkbox[i].checked === true){                    
                    ac.push(checkbox[i].value);                                        
                }                  
            }
            return ac;
        }

        function getCheckBoxSelected(e){
            e.preventDefault();               
            var $checkbox = doc.querySelectorAll('input[name="check_id"]');
            var ac = [];                       

            ac = getCheckBox($checkbox)

            if (ac.length == 0){
                $('[data-js="modal_checkbox"]').modal();
            }
            else{
                
                $form_modal_hidden_values_checkbox.setAttribute('value',ac);
                $form_modal.setAttribute('action',$click_checkbox.getAttribute('data-url'));                
                $('[data-js="modal_delete_all"]').modal();
            }
        }        
    
        function handleClickCheckBoxAll(e){        
            var $checkbox = doc.querySelectorAll('input[name="check_id"]');
            if (e.target.checked === true){
                mark_or_unmark(true)
            }
            else{
                mark_or_unmark(false)
            }
            function mark_or_unmark(check){
                for (var i=0; i < $checkbox.length; i++){
                    $checkbox[i].checked = check;            
                }
            }
        }      
        
        handleClickDelete();                                    
        on('[data-js="click_checkbox"]', 'click', getCheckBoxSelected);
        on('[data-js="check_all"]', 'click', handleClickCheckBoxAll);       

    });//DOMContentLoaded

})(document,window);