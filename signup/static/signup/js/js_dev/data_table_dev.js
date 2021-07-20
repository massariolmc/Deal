(function(doc,win){
    doc.addEventListener("DOMContentLoaded", function() {
        'use strict';
        var $search = doc.querySelector('[data-js="search"]');
        var $lines = doc.querySelector('[data-js="select_lines"]');
        var $table = doc.querySelector('#table_list');   
        var $modal_link = doc.querySelector('[data-js="modal_link_delete"]');              
        var page = 1;           

        function handleSearch(e){              
            $.ajax({
                type: "GET",                
                url: $table.getAttribute("data-url"),
                data: {'q': $search.value, 'l':$lines.value, 'page': page },
                dataType: "json",
                beforeSend : function(){
                    
                },
                success: function(data){                                
                    $table.innerHTML = data.html_signup_list;                                        
                    on('.click_page', 'click', handlePage);  
                    handleClickDelete();
                },
                failure: function(data){
                    
                },
            });                         
        }        

        function handlePage(e) {   
            console.log("e",e)     
            e.preventDefault();
            //page = e.target.href.slice(35);
            page = e.target.href.split("=", 2)[1];
            //console.log("e",page)  
            handleSearch();                
        };      

        function on(element, event, callback){
            doc.querySelector(element).addEventListener(event,callback,false);
        }    
        
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
           
        $search.addEventListener('input', handleSearch,false);
        $lines.addEventListener('change', handleSearch,false);
        on('.click_page', 'click', handlePage);
       

    });//DOMContentLoaded

})(document,window);