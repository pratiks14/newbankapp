$('.navbuttons').delegate('.continue3','click',function(){
    var formData = new FormData($('form')[0]);
    var empty = false;
    
    
    for (var [key, value] of formData.entries()) { 
        if (value == ''){
            empty = true;
            
            break;
        }
    }
    if(empty){
        var modalcontent = `
                            <div class="modal-body ">  
                            <h5><i class="fas fa-exclamation-circle"></i> Fill all the Inputs before continuing</h5>
                            </div>
                            <div class="modal-footer d-flex justify-content-start">
                            <button type="button" style="background-image:linear-gradient(#ddd,#bbb,#ddd);color:#111;" data-dismiss="modal" >Close</button>
                            </div>`;
        $('.modal-content').html(modalcontent);
        $('#dataModal').modal('show');
    }
    else{
        formData.append("registerno",3)
        $.ajax({
            type:'POST',
            url:'/register',
            processData:false,
            contentType:false,
            data:formData,
            success :function(data){
                for(var [key,value] of formData.entries() ){
                    window.sessionStorage[key] = value;
                }
                $('.content p:nth-child(1)').html('<h4>Your Details</h4>');

                $('.content p:nth-child(2)').html('');
                var form = `
                <br>
                <br>
                <div class="col-4">
                    <label >Username :</label>
        
                </div>
                
                <div class="col-8 row">
        
                        <div class="col-6 " style="vertical-align: middle;">
                            <input type="text" style="" class="form-control-plaintext" name="password" value="`+window.sessionStorage['username']+`" required>

                        </div>
                        <div class="col-6 " style="display:none">
                            
        
                        </div>
        
                </div>
                <br>
                <br>
                <div class="col-4">
                    <label >Password :</label>
        
                </div>
                
                <div class="col-8 row">
        
                        <div class="col-6 " style="vertical-align: middle">
                            <input type="password" style="" class="form-control-plaintext"  value="`+window.sessionStorage['userpassword']+`" required>
                        </div>
                        <div class="col-6 verification" >
                        <i class="far fa-eye eye pointer"></i>
                
                        </div>
        
                </div>
                <br>
                <br>
                <div class="col-4">
                    <label >Security Number :</label>
        
                </div>
                
                <div class="col-8 row">
        
                        <div class="col-6 " style="vertical-align: middle">
                        <input type="text"  class="form-control-plaintext" name="password" value="`+window.sessionStorage['securitynumber']+`" required>
                        </div>
                        <div class="col-6 verification" style="display:none">
                            
        
                        </div>
        
                </div>
                `;
                $('form').html(form);
                nextactive = $('.bread-crumb .active').next();
                $('.bread-crumb .active').removeClass('active').addClass('done');
                nextactive.addClass('active');
                $('.continue3').removeClass('continue3').addClass('confirm');
                $('.confirm').html('Confirm');
                $('.eye').click(function(){
                    if($(this).parent().parent().find('input').attr('type') == 'password'){
                        $(this).parent().parent().find('input').attr('type','text');
                        $(this).removeClass('fa-eye').addClass('fa-eye-slash');
                    }
                    else{
                        $(this).parent().parent().find('input').attr('type','password');
                        $(this).removeClass('fa-eye-slash').addClass('fa-eye');
                    }
                });
            },
            error:function(data){
                var modalcontent = `
                <div class="modal-body ">  
                <h5><i class="fas fa-exclamation-circle"></i> `+data.responseJSON+`</h5>
                </div>
                <div class="modal-footer d-flex justify-content-start">
                <button type="button" style="background-image:linear-gradient(#ddd,#bbb,#ddd);color:#111;" data-dismiss="modal" >Close</button>
                </div>`;
                $('.modal-content').html(modalcontent);
                $('#dataModal').modal('show');
            }

        });
    }

}); 

$('.navbuttons').delegate('.confirm','click',function(){
    var data = new FormData();
    for(var i =0; i < window.sessionStorage.length; i++){
        data.append(sessionStorage.key(i),window.sessionStorage.getItem(window.sessionStorage.key(i)));
     }
    
    data.set("registerno","confirm");
    // setTimeout(function(){
    //                 window.location.href = '/main';
    //             },1500);
    for (var [key, value] of data.entries()) { 
        console.log(key,value);
    }

    $.ajax({
        type:'POST',
        url:'/register',
        processData:false,
        contentType:false,
        data:data,
        success:function(data){
            var modalcontent = `
                <div class="modal-body ">  
                <h5><i class="far fa-check-square" style="color:green"></i> Registered</h5>
                <hr>
                <p>Loading Your Home Page</p>
               
                </div>`;
                $('.modal-content').html(modalcontent);
                $('#dataModal').modal('show');
                window.sessionStorage.clear();
                setTimeout(function(){
                    window.location.href = '/main';
                },1500);
        },
        error:function(data){
            var modalcontent = `
            <div class="modal-body ">  
            <h5><i class="fas fa-exclamation-circle"></i> `+data.responseJSON+`</h5>
            </div>
            <div class="modal-footer d-flex justify-content-start">
            <button type="button" style="background-image:linear-gradient(#ddd,#bbb,#ddd);color:#111;" data-dismiss="modal" >Close</button>
            </div>`;
            $('.modal-content').html(modalcontent);
            $('#dataModal').modal('show');
            
        }
    });
    
});
