import React, { useEffect } from 'react';
import icon01 from '../images/sub/btn_icon01.png';
import icon02 from '../images/sub/btn_icon02.png';
import icon03 from '../images/sub/btn_icon03.png';
import Box from '@mui/material/Box';
import Search from '../components/Search';

import ExclusiveSelect from '../components/ExclusiveSelect';
import graphImage from '../images/sub/graph_img.jpg';
import useFetch from '../hooks/useFetch';
import { getLineBreakText } from '../js/util';

const timeBefore = (today: Date, timelength: String) => {
  const [d, m, y] = [today.getDate(), today.getMonth(), today.getFullYear()];
  if (timelength === '1d') {
    return new Date(y, m, d - 1);
  }
  if (timelength === '1wk') {
    return new Date(y, m, d - 7);
  }
  if (timelength === '1m') {
    return new Date(y, m - 1, d);
  }
  if (timelength === '1y') {
    return new Date(y - 1, m, d);
  }
  if (timelength === 'all') {
    return new Date(2000, 0, 1);
  }
};

const RiskReport = () => {
  const [dateRange, setDateRange] = React.useState('all'); // for period select
  const { data, isPending, error } = useFetch(
    '/static/ReportData.example.json'
  );

  const loadingScreen = (
    <section id="sub_contents">
      <div className="sub01_wrap">
        <h2 className="h2_tit2">Loading...</h2>
      </div>
      <div className="content clfix"></div>
    </section>
  );

  const errorScreen = (
    <section id="sub_contents">
      <div className="sub01_wrap">
        <h2 className="h2_tit2">Error</h2>
      </div>
      <div className="content clfix"></div>
    </section>
  );

  useEffect(() => {
    if (data) {
      setDateRange(data.dateRange);
    }
  }, [data]);

  const selectHandler = (dateRange) => {
    alert('dateRange changed ' + dateRange);
    // TODO: call search here
  };

  return (
    <>
      {isPending ? (
        loadingScreen
      ) : error ? (
        errorScreen
      ) : (
        <section id="sub_contents">
          <div className="sub01_wrap">
            <h2 className="h2_tit2">
              “{data.topic}” 개요
              <em>
                {data.startDate}부터 {data.endDate}까지
              </em>
            </h2>

            <div className="text">{getLineBreakText(data.overview)}</div>

            <div className="period">
              <span>{data.startDate} 이후의 주요내용</span>
              <ExclusiveSelect
                selectOptions={['1d', '1wk', '1m', '1yr', 'all']}
                selectedValue={dateRange}
                setSelectedValue={setDateRange}
                selectHandler={selectHandler}
              />
            </div>

            <div className="content clfix">
              <div className="img">
                <img src={graphImage} alt="" />
              </div>
              <div className="text">
                {data.contents.map(({ title, summary }) => {
                  return (
                    <>
                      <h4>{title}</h4>
                      {getLineBreakText(summary)}
                    </>
                  );
                })}
              </div>
            </div>
          </div>
        </section>
      )}
    </>
  );
};

export default RiskReport;
