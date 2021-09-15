import React, { useState, useEffect } from 'react';
import { Menu, Button } from 'antd';
import styled from 'styled-components';
import { Link } from 'react-router-dom';
import Axios from 'axios';

const MenuList = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  .ant-menu {
    display: flex;
    justify-content: flex-end;
    width: 100%;
  }
`;

function NavBar() {

  const [auth, setAuth] = useState('')

  useEffect(() => {
    if (localStorage.getItem('token') !== null) {
      setAuth(true)
    }
  }, [])

  // fetch to axios 수정 
  const handleLogout = () => {
    let token = localStorage.getItem('token')

    Axios.post('/api/v1/user/auth/logout/', token)
      .then(res => {
        localStorage.clear()
        // 사용하려면 App.js에서 /로 라우팅해야 한다
        window.location.replace('/')
      });
  }

  return(
    <div>
      <MenuList>
        <Menu>
          { auth ?
            <Menu.Item key="logout" onClick={handleLogout}>
              로그아웃
            </Menu.Item>
            :
            <Menu.Item key="signin">
              <Link to="/login">
              로그인
              </Link>
            </Menu.Item>
          }
          { auth ?
            <></>
          :
            <Menu.Item key="signup">
              <Link to="/signup">
              회원가입
              </Link>
            </Menu.Item>
          }
        </Menu>
      </MenuList>
    </div>
  )
}

export default NavBar;