import React, { useState, useEffect } from 'react';
import Header from './components/Modal/Header';
import LoginModal from './components/Modal/LoginModal';
import InitInfo from './components/Modal/InitInfo';
import Board from './pages/Board';
import RiskReport from './pages/RiskReport';
import Secret from './pages/Secret';
import FakeNews from './pages/FakeNews';
import { Route } from 'react-router-dom';
import './App.css';


function App() {
  const [modal, setModal] = useState(false);
  const [user, setUser] = useState([])

  let [isAuthenticated, setisAuthenticated] = useState(localStorage.getItem('token') ? true : false)

  const userHasAuthenticated = (authenticated, username, token) => {
    setisAuthenticated(authenticated)
    setUser(username)
    console.log("토큰 저장됨");
    localStorage.setItem('token', token);
  }//회원가입이나 로그인이 성공했을 때 토큰을 저장

  const handleLogout = () => {
    setisAuthenticated(false)
    setUser("")
    localStorage.removeItem('token');
    setModal(false)
  }//로그아웃

  //회원가입이나 로그인이 성공했을 때 modal을 변경해 로그인 버튼을 없애고 정보 수정과 회원 탈퇴 버튼 나오게하는 setModal
  //useEffect의 두번째 인자는 모든 렌더링 후 두번째 인자가 변경될때에만 실행되라는 내용 
  useEffect(() => {
    if (isAuthenticated) {
      setModal(true)
    }
    else {
      setModal(false)
    }
  }, [isAuthenticated])



  return (
    <>
      <div className="App">
        <div className="auto-margin">
          <Header modal={modal} handleLogout={handleLogout} />
          <Route exact path="/">
            <Board />
          </Route>

          <Route exact path="/riskreport">
            <RiskReport user = {user}/>
          </Route>

          <Route exact path="/secret">
            <Secret />
          </Route>

          <Route exact path="/fakenews">
            <FakeNews />
          </Route>

          <Route exact path="/login">
            <LoginModal setModal={setModal} userHasAuthenticated={userHasAuthenticated} />
          </Route>

          <Route exact path="/init">
            <InitInfo />
          </Route>

        </div>
      </div>
    </>
  );
}

export default App;
