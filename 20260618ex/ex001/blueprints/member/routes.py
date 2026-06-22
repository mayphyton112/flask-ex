from flask import Blueprint, render_template, request, redirect, session
from utils.json_manager import load_members, save_members

member_bp = Blueprint(
    'member', 
    __name__,
    url_prefix='/member'
)

#signup_form
@member_bp.route('/signup_form', methods=['GET'])
def signup_form():#대부분은 실행함수를 그대로 쓴다.
    return render_template('signup_form.html')

# signup_confirm
@member_bp.route('/signup_confirm', methods=['post'])
def signup_confirm():
    mId = request.form['mId']
    mPw = request.form['mPw']
    mMail = request.form['mMail']
    mPhone = request.form['mPhone'] 

    members = load_members()

    #아이티 중복 체크
    if mId in members:
        return render_template('signup_result.html',
                               result = 'NG')

    members[mId] = {
        "mId": mId,
        "mPw": mPw,
        "mMail": mMail,
        "mPhone": mPhone,
    }
    save_members(members)
    return render_template('signup_result.html',
                           result = 'OK')

#signin_form
@member_bp.route('/signin_form', methods=['GET'])
def signin_form():

    result = request.args.get('result')

    return render_template('signin_form.html', result = result)

#signin_confirm
@member_bp.route('/signin_confirm', methods=['POST'])
def signin_confirm():
    mId = request.form['mId']
    mPw = request.form['mPw']
    
    members = load_members()
    
    if mId in members and members[mId]['mPw'] == mPw:
        session['signinedMemberId'] = mId
        return render_template('signin_result.html')
    
    return redirect('/member/signin_form?result=fail')

# /member/signout_confirm
@member_bp.route('/signout_confirm', methods=['GET'])
def signout_confirm():
    
    # session.clear()
    session.pop('signinedMemberId', None)

    return redirect('/')

# /member/modify_form
@member_bp.route('/modify_form')
def modify_form():
    members = load_members()
    member = members[session.get('signinedMemberId')] #현재 로그인된 회원정보 수집

    return render_template(
        'modify_form.html',
        member = member
    )

# /member/modify_confirm
@member_bp.route('/modify_confirm', methods=['post'])
def modify_confirm():

    '''
    현재 로그인 되어있는 회원 ID가 'gildong'이다.
    '''
    mId = request.form['mId']
    mPw = request.form['mPw']
    mMail = request.form['mMail']
    mPhone = request.form['mPhone']

    members = load_members()
    member = members[mId]
    member['mPw'] = mPw
    member['mMail'] = mMail
    member['mPhone'] = mPhone
    save_members(members)

    return render_template('modify_result.html')

# /member/delete_confirm
@member_bp.route('/delete_confirm')
def delete_confirm():
    members = load_members()
    signinedMemberId = session.get('signinedMemberId')
    del members[signinedMemberId]
    save_members(members)

    session.clear()

    return render_template('member/delete_result.html')