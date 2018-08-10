$('.navbuttons').delegate('.continue2','click',function(){
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
        formData.append("registerno",2)
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
                    $('.content p:nth-child(1)').html('Select security question which can be asked to verify you.');
                    $('.content p:nth-child(2)').html('');
                    var form = `
                    <div class="col-4 " >
                        <label style="margin-right:10px;"> <span style="color:#d00404">*</span>Required Field </label>
                        </div>
                        <div class="col-8"></div>
                        <br>
                        <br>
                        <div class="col-4">
                            <label><span style="color:#d00404">*</span>Select Question :</label>
                        </div>
                        <div class="col-8 row">

                                <div class="col-6 ">
                                    <select name="question" style="width:100%;">
                                        <option value="Your favourite food ?">Your favourite food ?</option>
                                        <option value="Your parent's place of birth ?">Your parent's place of birth ?</option>
                                        <option value="Your favourite color ?">Your favourite color ?</option>
                                        
                                    </select>
                                </div>


                        </div>
                        <br>
                        <br>
                        <!-- <br>
                        <br> -->
                        <div class="col-4">
                            <label ><span style="color:#d00404">*</span >Your Answer :</label>

                        </div>
                        <div class="col-8 row">

                            <div class="col-6 " style="vertical-align: middle">
                                <input type="text" style="width:100%;" name="answer" required>
                            </div>
                            <div class="col-6 verification" style="display:none">
                                
                            </div>
                        </div>
                    `;
                    $('form').html(form);
                    nextactive = $('.bread-crumb .active').next();
                    $('.bread-crumb .active').removeClass('active').addClass('done');
                    nextactive.addClass('active');
                    $('.continue2').removeClass('continue2').addClass('continue3')            
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
