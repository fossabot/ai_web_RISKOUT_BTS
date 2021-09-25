import React from 'react';
import icon01 from '../images/sub/btn_icon01.png'
import icon02 from '../images/sub/btn_icon02.png'
import icon03 from '../images/sub/btn_icon03.png'

const RiskReport = () => {
    let name = "user"
    return (
        <>
        <section id="sub_contents">
		<div class="sub01_wrap">
			<h2 class="h2_tit">Welcome to Risk Out,{name}.</h2>
			<h3>AI로 고퀄리티 위협 현황 보고서를 작성</h3>
			<div class="period">
				<span>기간 : </span>
				<ul class="clfix">
					<li><button>1m</button></li>
					<li><button>6m</button></li>
					<li><button>YTD</button></li>
					<li><button>1y</button></li>
					<li><button>모두</button></li>
				</ul>
			</div>
			<div class="category">
				<span>카테고리</span>
				<ul class="clfix">
					<li class="on"><button>
						<div class="img"><img src={icon01} alt=""/></div>
						<p>북한</p>
					</button></li>
					<li><button>
						<div class="img"><img src={icon02} alt=""/></div>
						<p>테러리스트</p>
					</button></li>
					<li><button>
						<div class="img"><img src={icon03} alt=""/></div>
						<p>해커</p>
					</button></li>
				</ul>
				<button class="submit">작성</button>
			</div>
		</div>
	</section>
    </>
    );
};

export default RiskReport;