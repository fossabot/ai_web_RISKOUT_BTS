import React, { useState } from 'react';
import { useHistory } from 'react-router'
import '../../css/LoginModal.css';

const InitInfo = (props) => {
let [useremail, setUserEamil] = useState()
const data = {email : useremail}

const handleEmailChange = (e) => {
  setUserEamil(e.target.value)
}

    const history = useHistory()
    return (
        <div className="login-container">
        <div className="login-box">
          <span>비밀번호 찾기</span>
              <center>
            <input type="text" placeholder="이메일을 입력하세요." onChange={handleEmailChange}/>
            <br></br>
            <div><span>이메일로 임시 비밀번호를 보내 드립니다.</span></div>
            <br></br>
            <button className="JoinLoign-button" onClick={(e)=>{
                  e.preventDefault()
                  alert(JSON.stringify(data))
                    fetch('/api/password_reset/', {
                      method: 'POST',
                      headers:{
                        'Content-Type': 'application/json'
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

export default InitInfo;