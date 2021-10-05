import React, { useState } from 'react';
import { useHistory } from 'react-router'
import '../../css/LoginModal.css';

const PasswordResetPage = (props) => {
  let [userpassword, setUserPassword] = useState()
  let [userpasswordCheck, setUserPasswordCheck] = useState();
  let usertoken = document.URL.split("=")[1];


  const data = {password : userpassword,token : usertoken, }

const handlePassword1Change = (e) => {
  setUserPassword(e.target.value)
}

const handlePassword2Change = (e) => {
  setUserPasswordCheck(e.target.value)
}

    const history = useHistory()
    return (
        <div className="login-container">
        <div className="login-box">
          <span>비밀번호 초기화</span>
              <center>
            <input type="password" placeholder="새 비밀번호 입력" onChange={handlePassword1Change}/>
            <br></br>
            <input type="password" placeholder="새 비밀번호 확인" onChange={handlePassword2Change}/>
            <br></br>
            <button className="JoinLoign-button" onClick={(e)=>{

                  e.preventDefault()
                  alert(JSON.stringify(data))
                  if(userpassword !== userpasswordCheck){
                    alert("비밀번호가 서로 일치하지 않습니다!")
                  }else{
                    fetch('/api/password_reset/confirm/', {
                      method: 'POST',
                      headers:{
                        'Content-Type': 'application/json'
                      },
                      body: JSON.stringify(data)
                    }).then(res => res.json())
                    .then(json => {
                      if(json.status==="OK"){
                          alert("성공적으로 변경되었습니다.");
                          history.push("/");
                      }else{
                          alert("비밀번호를 다시 확인 해 주세요.")
                      }
                    })
                    .catch(error => alert(error));
                    };

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

export default PasswordResetPage;