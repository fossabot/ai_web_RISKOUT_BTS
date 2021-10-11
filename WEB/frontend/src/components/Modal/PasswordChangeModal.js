import { Grid,Paper, Avatar, TextField, Button, Typography,Link } from '@material-ui/core'
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import React, { useState } from 'react';
import { useHistory } from 'react-router'

const PasswordChangeModal=(props)=>{
  let [userpassword, setUserPassword] = useState()
  let [userpasswordCheck, setUserPasswordCheck] = useState();
  let token = localStorage.getItem("token");


  const data = {old_password : useroldpassword, new_password : usernewpassword}

const handlePassword1Change = (e) => {
  setUserPassword(e.target.value)
}

const handlePassword2Change = (e) => {
  setUserPasswordCheck(e.target.value)
}

    const history = useHistory()

    const paperStyle={padding :40,height:'70vh',width:800, margin:"20px auto"}
    const avatarStyle={backgroundColor:'#1bbd7e'}
    const btnstyle={margin:'10px 0'}
    return(
      <>
      <br></br>
      <br></br>
      <br></br>
      <Grid>
      <Paper elevation={10} style={paperStyle}>
          <Grid align='center'>
               <Avatar style={avatarStyle}><LockOutlinedIcon/></Avatar>
              <h2>비밀번호 변경</h2>
          </Grid>
          <TextField label='기존 비밀번호' placeholder='기존 비밀번호를 입력해 주세요.' type='password' fullWidth required  onChange={handlePassword1Change}/>
          <TextField label='새 비밀번호 확인' placeholder='새 비밀번호를 다시 입력해 주세요.' type='password' fullWidth required  onChange={handlePassword2Change}/>
          <Button type='submit' color='primary' variant="contained" style={btnstyle} fullWidth className="JoinLoign-button"onClick={(e)=>{

            e.preventDefault()
            alert(JSON.stringify(data))
            alert(token)
             fetch('/api/change-password/', {
             method: 'PUT',
             headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`,
             },
             body: JSON.stringify(data)
             }).then(res => res.json())
            .then(json => {
            if(json.code===200){
                 alert("성공적으로 변경되었습니다.");
                   history.push("/");
              }else{
          alert("비밀번호를 다시 확인 해 주세요.")
            }
         })
     .catch(error => alert(error));
    }
        }>전송</Button>
          <Typography >
          <br></br>
               <Link href="/login" >
                  로그인
          </Link>
          </Typography>
      </Paper>
  </Grid>
  </>
    )
}

export default PasswordChangeModal