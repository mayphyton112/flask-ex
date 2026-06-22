function signupForm() {
    console.log('signupForm() CALLED!!')

    let form = document.signup_form;

    let mId = form.mId.value.trim();
    let mPw = form.mPw.value.trim();
    let mMail = form.mMail.value.trim();
    let mPhone = form.mPhone.value.trim();
    
    if (mId === "") {
        alert("Please input member ID");
        form.mId.focus();
        
    } else if (mPw === "") {
        alert("Please input member PW");
        form.mPw.focus();

    } else if (mMail === "") {
        alert("Please input member MAIL");
        form.mMail.focus();

    } else if (mPhone === "") {
        alert("Please input member PHONE");
        form.mPhone.focus();

    } else {
        form.submit();

    }

}

function signinForm() {
    console.log('signinForm() CALLED!!')

    let form = document.signin_form;

    let mId = form.mId.value.trim();
    let mPw = form.mPw.value.trim();
    
    if (mId === "") {
        alert("Please input member ID");
        form.mId.focus();
        
    } else if (mPw === "") {
        alert("Please input member PW");
        form.mPw.focus();

    } else {
        form.submit();

    }

}

function modifyForm() {
    console.log('modifyForm() CALLED!!')

    let form = document.modify_form;

    let mPw = form.mPw.value.trim();
    let mMail = form.mMail.value.trim();
    let mPhone = form.mPhone.value.trim();
    
    if (mPw === "") {
        alert("Please input member PW");
        form.mPw.focus();

    } else if (mMail === "") {
        alert("Please input member MAIL");
        form.mMail.focus();

    } else if (mPhone === "") {
        alert("Please input member PHONE");
        form.mPhone.focus();

    } else {
        form.submit();

    }

}