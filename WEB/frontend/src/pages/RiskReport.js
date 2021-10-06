import React, { useEffect } from 'react';
import icon01 from '../images/sub/btn_icon01.png';
import icon02 from '../images/sub/btn_icon02.png';
import icon03 from '../images/sub/btn_icon03.png';
import Box from '@mui/material/Box';
import Search from '../components/Search';
import { Chip, Stack, Link, Grid } from '@mui/material';

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
    '/static/ReportData.example.json?dateRange=' + dateRange // fetch occurs whenever dateRange changes
  );

  /*
    // if using POST request with request options
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        topic: 'Hacker', // organization name?
        dateRange: dateRange, // user selected
        articleIds: [1, 2, 3], // get from sessionStorage
      }),
    }
  */

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

  // select handler is not required.
  // when dateRange changes selected happens due to the useFetch hook
  const selectHandler = (dateRange) => {
    alert('dateRange changed ' + dateRange);
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
              Report
              <em>
                {new Intl.DateTimeFormat('ko-KR', { dateStyle: 'full' }).format(
                  new Date()
                )}{' '}
                (24h)
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
                {data.contents.map(
                  ({
                    title,
                    summary,
                    characteristics,
                    sourceName,
                    url,
                    datetime,
                  }) => {
                    return (
                      <article>
                        <Link
                          href={url}
                          target="_blank"
                          rel="noopener"
                          underline="hover"
                        >
                          <h4>{title}</h4>
                        </Link>
                        {getLineBreakText(summary)}
                        <Grid
                          container
                          direction="row"
                          justifyContent="space-between"
                          alignItems="center"
                          sx={{ mt: '1rem' }}
                        >
                          <Stack direction="row" spacing={1}>
                            {characteristics.map((c) => (
                              <Chip
                                label={c}
                                variant="outlined"
                                size="medium"
                                sx={{ height: '2.4rem', fontSize: '1rem' }}
                              />
                            ))}
                          </Stack>
                          <Link
                            href={url}
                            target="_blank"
                            rel="noopener"
                            underline="hover"
                          >
                            <em>원본:</em> {sourceName} {datetime}
                          </Link>
                        </Grid>
                      </article>
                    );
                  }
                )}
              </div>
            </div>
          </div>
        </section>
      )}
    </>
  );
};

export default RiskReport;
