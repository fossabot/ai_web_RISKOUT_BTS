import React, { useState } from 'react';
import { useHistory } from 'react-router'
import '../../css/LoginModal.css';

const PasswordChangePage = (props) => {
  let [useroldpassword, setUserOldPassword] = useState()
  let [usernewpassword, setUserNewPassword] = useState();
  let token = props.token;

  const data = {old_password : useroldpassword, new_password : usernewpassword}

const handlePassword1Change = (e) => {
  setUserOldPassword(e.target.value)
}

const handlePassword2Change = (e) => {
  setUserNewPassword(e.target.value)
}

    const history = useHistory()
    return (
        <div className="login-container">
        <div className="login-box">
          <span>비밀번호 변경</span>
              <center>
            <input type="password" placeholder="기존 비밀번호 입력" onChange={handlePassword1Change}/>
            <br></br>
            <input type="password" placeholder="새 비밀번호 입력" onChange={handlePassword2Change}/>
            <br></br>
            <button className="JoinLoign-button" onClick={(e)=>{

                  e.preventDefault()
                  alert(JSON.stringify(data))
                  alert(token)
                    fetch('/api/change-password/', {
                      method: 'PUT',
                      headers:{
                        'Authorization': token
                      },
                      body: JSON.stringify(data)
                    });


                  }
                  }
                 
                >전송</button>
                <br></br>
                <div className="foot-link" onClick={(e)=>{
                e.preventDefault()
                  history.push('/login');
                }}>로그인</div>
                </center>
        </div>
    </div>
    );
};

export default PasswordChangePage;