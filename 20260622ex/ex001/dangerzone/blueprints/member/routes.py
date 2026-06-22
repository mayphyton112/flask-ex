from flask import Blueprint, render_template, request, redirect, session
from utils.json_manager import load_members, save_members

member_bp = Blueprint(
    'member',
    __name__,
    url_prefix='/member'
)

# 회원 가입 양식
@member_bp.route('/signup_form', methods=['GET'])
def signup_form():
    return render_template('member/signup_form.html')

# 회원 가입 확인
@member_bp.route('/signup_confirm', methods=['POST'])
def signup_confirm():
    print('signup_confirm() CALLED!!')

    mId = request.form['mId']
    mPw = request.form['mPw']
    mMail = request.form['mMail']
    mPhone = request.form['mPhone']

    members = load_members()

    if mId in members:
        return render_template(
            '/member/signup_result.html', 
            result = 'NG')

    members[mId] = {
        "mId": mId,
        "mPw": mPw,
        "mMail": mMail,
        "mPhone": mPhone
    }

    save_members(members)

    return render_template(
        '/member/signup_result.html', 
        result = 'OK')

# 회원 로그인 양식
@member_bp.route('/signin_form', methods=['GET'])
def signin_form():

    result = request.args.get('result')

    return render_template(
        'member/signin_form.html', 
        result = result
        )

# 회원 로그인 확인
@member_bp.route('/signin_confirm', methods=['POST'])
def signin_confirm():
    print('signin_confirm() CALLED!!')

    mId = request.form['mId']
    mPw = request.form['mPw']

    members = load_members()

    if members[mId] != None and members[mId]['mPw'] == mPw:
        session['signinedMemberId'] = mId
        return render_template('/member/signin_result.html')
    
    return redirect('/member/signin_form?result=fail')

# 회원 로그아웃
@member_bp.route('/signout_confirm', methods=['GET'])
def signout_confirm():
    print('signout_confirm() CALLED!!')

    session.clear()

    return redirect('/')

# 회원 정보 수정 양식
@member_bp.route('/modify_form', methods=['GET'])
def modify_form():
    print('modify_form() CALLED!!')

    members = load_members()
    signinedMemberId = session.get('signinedMemberId')
    member = members[signinedMemberId]

    return render_template(
        'member/modify_form.html',
        member = member
    )
    

# 회원 정보 수정 확인
@member_bp.route('/modify_confirm', methods=['POST'])
def modify_confirm():
    print('modify_confirm() CALLED!!')

    mId = request.form['mId']
    mPw = request.form['mPw']
    mMail = request.form['mMail']
    mPhone = request.form['mPhone']

    members = load_members()
    members[mId]['mPw'] = mPw
    members[mId]['mMail'] = mMail
    members[mId]['mPhone'] = mPhone

    save_members(members)

    return render_template('/member/modify_result.html')


# 회원 탈퇴
@member_bp.route('/delete_confirm', methods=['GET'])
def delete_confirm():
    print('delete_confirm() CALLED!!')

    members = load_members()
    signinedMemberId = session.get('signinedMemberId')
    del members[signinedMemberId]

    save_members(members)

    session.clear()

    return render_template('/member/delete_result.html')


