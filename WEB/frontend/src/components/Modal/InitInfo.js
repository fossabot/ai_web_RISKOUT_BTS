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
          <div className="exit">
              <button onClick={()=>{ history.goBack()}}>
                <svg stroke="currentColor" fill="currentColor" viewBox="0 0 24 24" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"></path></svg>
              </button>
          </div>
          <span>비밀번호 찾기</span>
              <center>
            <input type="text" placeholder="이메일을 입력하세요." onChange={handleEmailChange}/>
            <br></br>
            <div><span>이메일로 임시 비밀번호를 보내 드립니다.</span></div>
            <br></br>
            <button className="JoinLoign-button" onClick={(e)=>{
                  e.preventDefault()
                  
                    fetch('http://localhost:8000/initpwd/', {
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