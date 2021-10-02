import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router';
import { Link } from 'react-router-dom';
// import '../../css/Header.css';
import logo from '../../images/sub/logo_w.png';
import logo_btn from '../../images/sub/prev_btn.png';

function Header(props) {
  let [userprofile, setUserprofile] = useState(false);
  let [userPhoto, setUserPhoto] = useState();
  let [currentUser_pk, setCurrentUser_pk] = useState();

  useEffect(() => {
    fetch('http://localhost:8000/user/current/', {
      headers: {
        Authorization: `JWT ${localStorage.getItem('token')}`,
      },
    })
      .then((res) => res.json())
      .then((json) => {
        // 현재 유저 정보 받아왔다면, 로그인 상태로 state 업데이트 하고
        if (json.id) {
          //유저정보를 받아왔으면 해당 user의 프로필을 받아온다.
        }
        fetch(
          'http://localhost:8000/user/auth/profile/' + json.id + '/update/',
          {
            method: 'PATCH',
            headers: {
              Authorization: `JWT ${localStorage.getItem('token')}`,
            },
          }
        )
          .then((res) => res.json())
          .then((userData) => {
            setUserPhoto(userData.photo);
            setCurrentUser_pk(userData.user_pk);
          })
          .catch((error) => {
            console.log(error);
          });
      })
      .catch((error) => {
        console.log(error);
      });
  }, [userPhoto]);
  const history = useHistory();

  return (
    <>
      <header id="sub_header">
        <Link to="/">
          <h1>
            <img src={logo} alt="logo" />
          </h1>
        </Link>
        <button
          onClick={() => {
            history.goBack();
          }}
          className="prev_btn"
        >
          <img src={logo_btn} alt="/" />
        </button>
        <ul className="sub_menu">
          <li>
            <Link to="/">언론 동향</Link>
          </li>
          <li>
            <Link to="/secret">탐지 현황</Link>
          </li>
          <li>
            <Link to="/riskreport">리포트</Link>
          </li>
          {props.modal === false ? ( // not logged in
            <li>
              <Link to="/login">로그인</Link>
            </li>
          ) : (
            <li>
              <Link onClick={props.handleLogout} to="/">
                로그 아웃
              </Link>
            </li>
          )}
        </ul>
        <p className="copyright">
          Copyright © 2021. RISKOUT All right reserved.
        </p>
      </header>
    </>
  );
}

export default Header;
