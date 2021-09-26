import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router'
import { Link } from 'react-router-dom';
import '../../css/Header.css';
import logo from '../../images/sub/logo_w.png'
import logo_btn from '../../images/sub/prev_btn.png'

function Header(props) {

  let [userprofile, setUserprofile] = useState(false)
  let [userPhoto, setUserPhoto] = useState()
  let [currentUser_pk, setCurrentUser_pk] = useState();

 
  const history = useHistory()
  return (
    <>
      <header id="sub_header">

        <Link to="/"><h1><img src={logo} alt="logo" /></h1></Link>
        <button onClick={() => { history.goBack() }} class="prev_btn">
          <img src={logo_btn} alt="/" /></button>
        <ul class="sub_menu">
          <li><Link to="/riskreport">위협 보고</Link></li>
          <li ><Link to="/secret">기밀 유출 현황</Link></li>
          <li><Link to="/fakenews">허위 정보 검사</Link></li>
          {
            props.modal === false // not logged in
              ? <li><Link to="/login">로그인</Link></li>
              : <li><Link onClick={props.handleLogout} to="/">로그 아웃</Link></li>
          }
        </ul>
        <p class="copyright">Copyright © 2021. RISKOUT All right reserved.</p>
      </header>
    </>
  )
}

export default Header;