import React, { useState, useEffect } from 'react';
import Header from '../components/Modal/Header';
import Navi from '../components/Modal/Navi'
import LoginModal from '../components/Modal/LoginModal';
import Profile from '../components/User/Profile';
import { Route } from 'react-router-dom';
import '../App.css';
import './css/style.css'
import Write from '../components/Board/Write';
import Detail from '../components/Board/Detail';
import Update from '../components/Board/Update';
import Mysite from '../components/User/Mysite';
import Board from '../components/Board/Board';

function App() {

    return (
    <>
      <div id="wrap">
	<header id="sub_header">
		<h1><a href="#"><img src={process.env.PUBLIC_URL + "/images/sub/logo_w.png"} alt=""/></a></h1>
		<button className="prev_btn"><img src={process.env.PUBLIC_URL + "/images/sub/prev_btn.png"} alt=""/></button>
		<ul className="sub_menu">
			<li className="on"><a href="">위협보고</a></li>
			<li><a href="">기밀 유출 현황</a></li>
			<li><a href="">허위 정보 검사</a></li>
			<li><a href="">로그아웃</a></li>
		</ul>
		<p className="copyright">Copyright © 2021. RISKOUT All right reserved.</p>
	</header>

	<section id="sub_contents">
		<div className="sub01_wrap">
			<h2 className="h2_tit">Welcome to Risk Out, 민석.</h2>
			<h3>AI로 고퀄리티 위협 현황 보고서를 작성</h3>
			<div className="period">
				<span>기간 : </span>
				<ul className="clfix">
					<li><button>1m</button></li>
					<li><button>6m</button></li>
					<li><button>YTD</button></li>
					<li><button>1y</button></li>
					<li><button>모두</button></li>
				</ul>
			</div>
			<div className="category">
				<span>카테고리</span>
				<ul className="clfix">
					<li className="on"><button>
						<div className="img"><img src={process.env.PUBLIC_URL + "/images/sub/btn_icon01.png"} alt=""/></div>
						<p>북한</p>
					</button></li>
					<li><button>
						<div className="img"><img src={process.env.PUBLIC_URL + "/images/sub/btn_icon02.png"} alt=""/></div>
						<p>테러리스트</p>
					</button></li>
					<li><button>
						<div className="img"><img src={process.env.PUBLIC_URL + "/images/sub/btn_icon03.png"} alt=""/></div>
						<p>해커</p>
					</button></li>
				</ul>
				<button className="submit">작성</button>
			</div>
		</div>
	</section>

  </div>
    </>
    );
}

export default App;