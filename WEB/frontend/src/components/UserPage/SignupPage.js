import React, { useState } from 'react';
import Axios from 'axios';
import { Input } from 'antd';
import styled from 'styled-components';

const SignupDiv = styled.div`
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

const SignupPage = () => {
  const [email, setEmail] = useState('')
  const [password1, setPassword1] = useState('')
  const [password2, setPassword2] = useState('')
  const [errors, setErrors] = useState(false)

  const onChangeEmail = (e) => {
    setEmail(e.target.value)
  }

  const onChangePwd1 = (e) => {
    setPassword1(e.target.value)
  }

  const onChangePwd2 = (e) => {
    setPassword2(e.target.value)
  }

  const onSubmit = (e) => {
    e.preventDefault()

    const user = {
      email: email,
      password1: password1,
      password2: password2
    }

    // 유효성 검사
    if(password1 !== password2) {
      alert('비밀번호와 비밀번호 확인이 일치하지 않습니다')
      return false
    }

    Axios.post('/api/v1/user/auth/register/', user)
      .then(res => {
        if (res.data.key) {
          localStorage.clear()
          localStorage.setItem('token', res.data.key)
          // 사용하려면 App.js에서 /로 라우팅해야 한다
          window.location.replace('/')
        } else {
          setEmail('')
          setPassword1('')
          setPassword2('')
          localStorage.clear()
          setErrors(true)
        }
      })
      .catch(err => {
        console.clear()
        alert('아이디 혹은 비밀번호가 일치하지 않습니다')
      })
  }

  return (
    <SignupDiv>
      <h1>회원가입</h1>
      <br />
      {errors === true && <h2>Cannot signup with provided credentials</h2>}
      <form onSubmit={onSubmit}>
        <label htmlFor='email'>이메일 주소:</label>
        <Input
          type='email'
          value={email}
          onChange={onChangeEmail}
          required
        />
        <label htmlFor='password1'>비밀번호(소문자, 숫자, 특수문자 포함 8~16자):</label>
        <Input
          type='password'
          value={password1}
          onChange={onChangePwd1}
          minLength='8'
          pattern='^(?=.*[a-z])(?=.*\d)(?=.*[$@$!%*#?&])[a-z\d$@$!%*#?&]{8,16}$'
          required
        />
        <br />
        <label htmlFor='password2'>비밀번호 확인(소문자, 숫자, 특수문자 포함 8~16자):</label>
        <Input
          type='password'
          value={password2}
          onChange={onChangePwd2}
          minLength='8'
          pattern='^(?=.*[a-z])(?=.*\d)(?=.*[$@$!%*#?&])[a-z\d$@$!%*#?&]{8,16}$'
          required
        />
        <Input type='submit' size="large" value='가입하기' />
      </form>
    </SignupDiv>
  )
}

export default SignupPage;