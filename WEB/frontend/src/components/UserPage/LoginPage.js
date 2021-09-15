import React, { useState } from 'react';
import Axios from 'axios';
import { Input } from 'antd';
import styled from 'styled-components';

const LoginDiv = styled.div`
  padding: 3rem;
    form {
    width: 320px;
    display: inline-block;
    label {
      margin-bottom: 1rem;
    }
    input {
      margin-bottom: 1.5rem;
      &[type=submit] {
        background: black;
        color: white;
        margin-top: 1rem;
      }
    }
  }
`;

const LoginPage = () => {

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [errors, setErrors] = useState(false)

  const onSubmit = (e) => {
    e.preventDefault()

    const user = {
      email: email,
      password: password
    }

    Axios.post('/api/v1/user/auth/login/', user)
      .then(res => {
        if (res.data.key) {
          localStorage.clear()
          localStorage.setItem('token', res.data.key)
          // 사용하려면 App.js에서 /로 라우팅해야 한다
          window.location.replace('/')
        } else {
          setEmail('')
          setPassword('')
          localStorage.clear()
          setErrors(true)
        }
      })
      .catch(err => {
        console.clear()
        alert('아이디 또는 비밀번호가 일치하지 않습니다')
        setEmail('')
        setPassword('')
      })
  }

  return (
    <LoginDiv>
      <h1>로그인</h1>
      <br />
      {errors === true && <h2>Cannot log in with provided credentials</h2>}
        <form onSubmit={onSubmit}>
          <label>이메일 주소:</label>
          <Input
            type='email'
            value={email}
            required
            onChange={e => setEmail(e.target.value)}
          />
          <label>비밀번호:</label>
          <Input
            type='password'
            value={password}
            required
            onChange={e => setPassword(e.target.value)}
          />
          <Input type='submit' size="large" value='로그인' />
        </form>
    </LoginDiv>
  )
}

export default LoginPage;