import React, { useState, useEffect } from 'react';
import { Route } from 'react-router-dom';

import Layout from './layout';

import Board from './pages/Board';
import DetectionStatus from './pages/DetectionStatus';
import PressTrends from './pages/PressTrends';
import Dashboard from './pages/Dashboard';
import RiskReport from './pages/RiskReport';

import LoginModal from './components/Modal/LoginModal';
import RegisterModal from './components/Modal/RegisterModal';
import PasswordResetModal from './components/Modal/PasswordResetModal';
import InitInfo from './components/Modal/InitInfo';
import FilterTable from './components/FilterTable';
import Search from './components/Search';
import DynamicRoutes from "./DynamicRoutes";

import './App.css';
import './css/style.css';

function App() {
  const [modal, setModal] = useState(false);
  const [user, setUser] = useState([])

  let [isAuthenticated, setisAuthenticated] = useState(localStorage.getItem('token') ? true : false)

  const userHasAuthenticated = (authenticated, username, token) => {
    setisAuthenticated(authenticated)
    setUser(username)
    console.log("토큰 저장됨");
    localStorage.setItem('token', token);
  } //회원가입이나 로그인이 성공했을 때 토큰을 저장

  const handleLogout = () => {
    setisAuthenticated(false)
    setUser("")
    localStorage.removeItem('token');
    setModal(false)
  } //로그아웃

  //회원가입이나 로그인이 성공했을 때 modal을 변경해 로그인 버튼을 없애고 정보 수정과 회원 탈퇴 버튼 나오게하는 setModal
  //useEffect의 두번째 인자는 모든 렌더링 후 두번째 인자가 변경될때에만 실행되라는 내용 

  console.log(isAuthenticated)


  return (
    <>
    <div className="App">

  
          <Route exact path="/">
          <Layout handleLogout={handleLogout}>
            <Board />
            </Layout>
          </Route>
         <Route exact path="/presstrends">
         <Layout handleLogout={handleLogout}>
           <PressTrends />
           </Layout>
          </Route>

          <Route exact path="/detectionstatus">
          <Layout handleLogout={handleLogout}>
            <DetectionStatus />
            </Layout>
            </Route>

         <Route exact path="/riskreport">
         <Layout handleLogout={handleLogout}>
            <RiskReport />
          </Layout>
          </Route>

          <Route exact path="/login">
              <LoginModal setModal={setModal} userHasAuthenticated={userHasAuthenticated} />
            </Route>
            <Route exact path="/register">
              <RegisterModal setModal={setModal}/>
            </Route>
  
            <Route exact path="/init">
              <InitInfo setModal={setModal}/>
            </Route>
  
            <Route exact path="/password_reset">
              <PasswordResetModal setModal={setModal}/>
            </Route>
    </div>

      </>
  );
}

export default App;
