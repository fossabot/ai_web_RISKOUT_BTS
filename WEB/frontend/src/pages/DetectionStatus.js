import React, { useState, useEffect } from 'react';

import Search from '../components/Search';
import TableRow from '../components/SecretsTableRow';
import FilterCheckbox from '../components/FilterCheckbox';
import AppliedFilter from '../components/AppliedFilter';

import filtersCloseIcon from "../images/sub/filters_close.png";
import SecretsDetailModal from '../components/Modal/SecretsDetailModal';

function Secret() {

    const [isDetailModalOpen, setDetailModalOpen] = React.useState(false);
    const [detailModalData, setDetailModalData] = React.useState({
        "id": 0,
        "created_at": "",
        "site_url": "",
        "thumbnail_url": "",
        "category": "",
        "title": "",
        "contentBody": "",
        "summarized": "",
        "positivity": 0,
        "entities": {}
    });
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
        // console.log(`toggle ${hashtag}`, appliedFilters);
        if (appliedFilters.includes(hashtag)) {
            setAppliedFilters(appliedFilters.filter(val => val != hashtag));
        }
        else {
            appliedFilters.push(hashtag);
            setAppliedFilters([...appliedFilters]);
        }
    };

    const search = () => {
        // console.log(`search options: `);
        fetch('SecretData.example.json').then(res => res.json()).then((data) => {
            // console.log(data);
            setSearchResults(data);
        });
    };

    useEffect(search, [appliedFilters]); // changing filters automatically triggers search

    const showDetailModal = (id) => {
        const data = searchResults.contents.filter(x => x.id == id).pop(0); // popping doesn't affect original array
        console.log(data, searchResults.contents.filter(x => x.id == id), searchResults);
        setDetailModalData(data);
        setDetailModalOpen(true);
    };

    const scrapArticle = (id) => {
        console.log('TODO: scrap article ', id);
        alert("TODO: scrap article "+id);
    };
    
    const analyzePage = (id) => {
        console.log('TODO: analyzePage article ', id);
        alert("TODO: analyzePage article "+id);
        
    }

    return (
        <section id="sub_contents2">
            <div className="sub02_wrap clfix">
                <div className="sub02_con">
                    <div className="top_box">
                        <h2>탐지 현황</h2>
                        {/* <div className="search clfix">
                            <input type="text" placeholder="EX. 전투 세부 시행규칙" />
                            <button onClick={search}><img src={searchIcon} alt="" /></button>
                        </div> */}
                        <Search />
                    </div>



                    <h3>{searchResults.contentsLength}개 결과, {appliedFilters.length}개 필터 적용중</h3>
                    <ul className="filter_keyword clfix">
                        {
                            appliedFilters.map((filter, i) => <AppliedFilter hashtag={filter} onRemoveHashtag={toggleFilter} key={filter + i} />)
                        }
                    </ul>


                    {/* <div>{JSON.stringify(searchResults)}</div> */}

                    <table border="0" cellPadding="0" cellSpacing="0" className="tbl_type01">
                        <colgroup>
                            <col width="7%" />
                            <col width="65%" />
                            <col width="20%" />
                            <col width="8%" />
                        </colgroup>
                        <thead>
                            <tr>
                                <th>유형</th>
                                <th>제목</th>
                                <th>글쓴이</th>
                                <th>스크랩</th>
                            </tr>
                        </thead>
                        <tbody>
                            {
                                searchResults.contents.map((article, i) =>
                                    <TableRow
                                        id={article.id}
                                        title={article.title}
                                        preview={article.summarized}
                                        author={article.author}
                                        href={article.site_url}
                                        showDetailModal={showDetailModal}
                                        scrapArticle={scrapArticle}
                                        />)
                                    }
                            <TableRow
                                id="2"
                                title="해군 참모총장 만난 썰 푼다"
                                preview="나 사이버 작전센터에서 근무하는데 갑자기 참모총장이 와서 나랑 악수하는거임... 사진도 하나 찍혔어. 대박이더라. ㄷㄷ 그리고 끝나니까 무슨 동전같이 생긴거 받았는데 이게 참모총장?"
                                author="김남춘123"
                                href="naver.com"
                                showDetailModal={showDetailModal}
                                scrapArticle={scrapArticle}
                            />
                        </tbody>
                    </table>
                </div>




                <div className="sub02_filter">
                    <h4>Filters</h4>
                    <button><img src={filtersCloseIcon} alt="" className="close_btn" /></button>

                    {/* example
                    글에서 찾은 인물 
                    - [ ] 피해자
                    - [ ] 문재인
                    - [ ] 조정환
                    */}
                    {
                        [['단체', 'ORG'], ['인물', 'CVL'], ['시간대', 'TIM']].map(([filterLabel, filterCode]) => {

                            const filterTags = Object.entries(searchResults.filterTags[filterCode]);
                            return (

                                <div className="filter_con">
                                    <h5>글에서 찾은 {filterLabel}</h5>
                                    <span>{filterTags.length}</span>
                                    <ul className="keyword">
                                        {/* <FilterCheckbox count={10} hashtag="myHashtag" key="myHashtag" onToggle={toggleFilter} /> */}
                                        {
                                            filterTags.sort(([_, a], [__, b]) => a < b ? 1 : -1).map(([hashtag, freq], i) =>
                                                <FilterCheckbox count={freq} hashtag={hashtag} key={hashtag} onToggle={toggleFilter} checked={appliedFilters.includes(hashtag)} />
                                            )
                                        }
                                    </ul>
                                    <button className="more_btn">더보기</button>
                                </div>

                            );
                        })
                    }

                </div>
            </div>
            <SecretsDetailModal
                isOpen={isDetailModalOpen}
                setOpen={setDetailModalOpen}
                scrapArticle={scrapArticle}
                data={detailModalData}
            />
        </section>
    );
};

export default Secret;
