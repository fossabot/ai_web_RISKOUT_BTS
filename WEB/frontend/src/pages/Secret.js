import React, { useState, useEffect } from 'react';

import TableRow from '../components/SecretsTableRow';
import FilterCheckbox from '../components/FilterCheckbox';
import AppliedFilter from '../components/AppliedFilter';

import searchIcon from "../images/sub/search_icon.png";
import filtersCloseIcon from "../images/sub/filters_close.png";
// import exampleData from "./SecretData.example.json";

function Secret() {

    const [appliedFilters, setAppliedFilters] = useState(['전투시행세부규칙', 'GP/GOP']);
    const [searchResults, setSearchResults] = useState({
        "contentsLength": 0,
        "contents": [],
        "filterTags": {
            "ORG": {},
            "CVL": {},
            "TIM": {}
        }
    });


    const toggleFilter = hashtag => {
        console.log(`toggle ${hashtag}`);
        if (appliedFilters.includes(hashtag)) {
            setAppliedFilters(appliedFilters.filter(val => val != hashtag));
        }
        else {
            appliedFilters.push(hashtag);
            setAppliedFilters(appliedFilters);
        }
        search();
    };

    const search = () => {
        console.log(`search options: `);
        fetch('SecretData.example.json').then(res => res.json()).then((data) => {
            console.log(data);
            setSearchResults(data);
        });
    };

    useEffect(search, [appliedFilters]);

    return (
        <section id="sub_contents2">
            <div className="sub02_wrap clfix">
                <div className="sub02_con">
                    <div className="top_box">
                        <h2>탐지 현황</h2>
                        <div className="search clfix">
                            <input type="text" placeholder="EX. 전투 세부 시행규칙" />
                            <button onClick={search}><img src={searchIcon} alt="" /></button>
                        </div>
                    </div>



                    <h3>20 결과, 3 필터 적용중</h3>
                    <ul className="filter_keyword clfix">
                        {
                            appliedFilters.map((filter, i) => <AppliedFilter hashtag={filter} onRemoveHashtag={toggleFilter} key={filter + i} />)
                        }
                        {/* <AppliedFilter hashtag="전추세부시행규칙" onRemoveHashtag={toggleFilter} key="전추세부시행규칙" />
                        <AppliedFilter hashtag="KJCCS" onRemoveHashtag={toggleFilter} key="KJCCS" />
                        <AppliedFilter hashtag="GP/GOP" onRemoveHashtag={toggleFilter} key="GP/GOP" /> */}
                    </ul>


                    <div>{JSON.stringify(searchResults)}</div>

                    <table border="0" cellPadding="0" cellSpacing="0" className="tbl_type01">
                        <colgroup>
                            <col width="15%" />
                            <col width="65%" />
                            <col width="20%" />
                        </colgroup>
                        <thead>
                            <tr>
                                <th>유형</th>
                                <th>제목</th>
                                <th>글쓴이</th>
                            </tr>
                        </thead>
                        <tbody>
                            {
                                searchResults.contents.map((val, i) =>
                                    <TableRow
                                        title={val.title}
                                        preview={val.summarized}
                                    />)
                            }
                            <TableRow
                                title="해군 참모총장 만난 썰 푼다"
                                preview="나 사이버 작전센터에서 근무하는데 갑자기 참모총장이 와서 나랑 악수하는거임... 사진도 하나 찍혔어. 대박이더라. ㄷㄷ 그리고 끝나니까 무슨 동전같이 생긴거 받았는데 이게 참모총장?"
                                author="김남춘123"
                            />
                        </tbody>
                    </table>
                </div>




                <div className="sub02_filter">
                    <h4>Filters</h4>
                    <button><img src={filtersCloseIcon} alt="" className="close_btn" /></button>


                    <div className="filter_con">
                        <h5>글에서 찾은 단체</h5>
                        <span>{Object.entries(searchResults.filterTags.ORG).length}</span>
                        <ul className="keyword">
                            {
                                Object.entries(searchResults.filterTags.ORG).map(function ([hashtag, freq], i) {
                                    return <FilterCheckbox count={freq} hashtag={hashtag} key={hashtag} onToggle={toggleFilter} />;
                                })
                            }
                        </ul>
                        <button className="more_btn">더보기</button>
                    </div>
                    <div className="filter_con">
                        <h5>글에서 찾은 인물</h5>
                        <span>{Object.entries(searchResults.filterTags.CVL).length}</span>
                        <ul className="keyword">
                            {
                                Object.entries(searchResults.filterTags.CVL).map(function ([hashtag, freq], i) {
                                    return <FilterCheckbox count={freq} hashtag={hashtag} key={hashtag} onToggle={toggleFilter} />;
                                })
                            }
                        </ul>
                        <button className="more_btn">더보기</button>
                    </div>
                    <div className="filter_con">
                        <h5>글에서 찾은 시간대</h5>
                        <span>{Object.entries(searchResults.filterTags.TIM).length}</span>
                        <ul className="keyword">
                            {
                                Object.entries(searchResults.filterTags.TIM).map(function ([hashtag, freq], i) {
                                    return <FilterCheckbox count={freq} hashtag={hashtag} key={hashtag} onToggle={toggleFilter} />;
                                })
                            }
                        </ul>
                        <button className="more_btn">더보기</button>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default Secret;