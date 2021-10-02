import React, { useState } from "react";
import { useHistory } from "react-router";
import "../../css/LoginModal.css";

function LoginModal(props) {
  let [JoinLoign, setJoinLogin] = useState("로그인");
  const history = useHistory();

  let [username, setUsername] = useState();
  let [userpassword, setUserPassword] = useState();
  let [userpasswordCheck, setUserPasswordCheck] = useState();
  let [useremail, setUserEamil] = useState();

  const data = { username: username, password: userpassword, email: useremail };

  const handleNameChange = (e) => {
    setUsername(e.target.value);
  };
  const handlePasswordChange = (e) => {
    setUserPassword(e.target.value);
  };
  const handlePasswordCheckChange = (e) => {
    setUserPasswordCheck(e.target.value);
  };
  const handleEmailChange = (e) => {
    setUserEamil(e.target.value);
  };

  return (
    <>
      <div className="login-container">
        <div className="login-box">
          <div className="exit">
            <button
              onClick={() => {
                history.goBack();
              }}
            >
              <svg
                stroke="currentColor"
                fill="currentColor"
                viewBox="0 0 24 24"
                height="1em"
                width="1em"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"></path>
              </svg>
            </button>
          </div>
          <span>{JoinLoign}</span>
          <form>
            {JoinLoign === "로그인" ? (
              <>
                <input
                  type="text"
                  placeholder="아이디를 입력하세요"
                  onChange={handleNameChange}
                />
                <input
                  type="password"
                  placeholder="비밀번호를 입력하세요"
                  id="password"
                  onChange={handlePasswordChange}
                />
                <button
                  className="JoinLoign-button"
                  onClick={(e) => {
                    alert(JSON.stringify(data));
                    e.preventDefault();
                    fetch("/api/login/", {
                      method: "POST",
                      headers: {
                        "Content-Type": "application/json",
                      },
                      body: JSON.stringify(data),
                    })
                      .then((res) => res.json())
                      .then((json) => {
                        if (json.user && json.user.username && json.token) {
                          props.userHasAuthenticated(
                            true,
                            json.user.username,
                            json.token
                          );
                          history.push("/");
                          props.setModal(true);
                          console.log(json);
                        } else {
                          alert("아이디 또는 비밀번호를 확인해주세요.");
                        }
                      })
                      .catch((error) => alert(error));
                  }}
                >
                  {JoinLoign}
                </button>
              </>
            ) : (
              <>
                <input
                  type="text"
                  placeholder="아이디를 입력하세요"
                  onChange={handleNameChange}
                />

                <input
                  type="password"
                  placeholder="비밀번호를 입력하세요"
                  onChange={handlePasswordChange}
                />
                <input
                  type="password"
                  placeholder="비밀번호 확인"
                  onChange={handlePasswordCheckChange}
                />

                <input
                  type="text"
                  placeholder="이메일을 입력하세요."
                  onChange={handleEmailChange}
                />

                <button
                  className="JoinLoign-button"
                  onClick={(e) => {
                    alert(JSON.stringify(data));
                    e.preventDefault();
                    if (userpassword !== userpasswordCheck) {
                      alert("비밀번호를 확인해 주세요.");
                    } else {
                      fetch("/api/register/", {
                        method: "POST",
                        headers: {
                          "Content-Type": "application/json",
                        },
                        body: JSON.stringify(data),
                      })
                        .then((res) => res.json())
                        .then((json) => {
                          if (json.username && json.token) {
                            props.userHasAuthenticated(
                              true,
                              json.username,
                              json.token
                            );
                            history.push("/");
                            props.setModal(true);
                          } else {
                            alert("사용불가능한 아이디입니다.");
                          }
                        })

                        .catch((error) => alert(error));
                    }
                  }}
                >
                  가입
                </button>
              </>
            )}
          </form>
          <div className="login-foot">
            {JoinLoign === "회원가입" ? (
              <>
                <span>이미 회원이신가요 ?</span>
                <div
                  className="foot-link"
                  onClick={(e) => {
                    e.preventDefault();
                    setJoinLogin("로그인");
                  }}
                >
                  로그인
                </div>
              </>
            ) : (
              <>
                <center>
                  <div
                    className="foot-link"
                    onClick={(e) => {
                      e.preventDefault();
                      setJoinLogin("회원가입");
                    }}
                  >
                    회원가입
                  </div>
                  <br></br>
                  <br></br>
                  <div
                    className="foot-link"
                    onClick={(e) => {
                      e.preventDefault();
                      //비밀번호 경로 : /init
                      history.push("/init");
                    }}
                  >
                    비밀번호 찾기
                  </div>
                </center>
              </>
            )}
          </div>
        </div>
      </div>
    </>
  );
}

export default LoginModal;
