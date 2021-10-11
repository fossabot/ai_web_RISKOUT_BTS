import React, { useEffect, useRef } from 'react';
import {
  Box,
  Chip,
  Stack,
  Link,
  Grid,
  Typography,
  Skeleton,
  Card,
  CardMedia,
  CardContent,
} from '@mui/material';
import axios from 'axios';
import '../css/fonts.css';

import ExclusiveSelect from '../components/RiskReport/ExclusiveSelect';
import graphImage from '../images/sub/graph_img.jpg';
import useFetch from '../hooks/useFetch';
import { getLineBreakText, useSessionStorage } from '../js/util';
import ThreatMediaCard from '../components/RiskReport/ThreatMediaCard';
import PdfExportButton from '../components/RiskReport/PdfExportButton';
import Graphs from '../components/RiskReport/Graphs';
import ScrappedArticle from '../components/RiskReport/ScrappedArticle';
// import { Box } from '@mui/system';

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
  const [getCart, addCart] = useSessionStorage('riskoutShoppingCart');
  const [dateRange, setDateRange] = React.useState('all'); // for period select
  const { data, isPending, error } = useFetch(
    '/static/ReportData.example.json?dateRange=' +
      dateRange +
      '&articleIds=' +
      JSON.stringify(getCart()) // fetch occurs whenever dateRange changes
  );

  // => search
  useEffect(() => {
    const searchUrl = `/api/nlp/analyze/`;
    async function fetchSearch() {
      axios
        .post(searchUrl, {
          category: 'news',
          period: 72,
          tags: { PER: ['김정은'], LOC: ['북한'] },
          search_text: '노동신문',
          limit: 5,
          offset: 0,
        })
        .then((data) => {
          console.log(data.data);
        });
    }
    fetchSearch();
  }, []);

  const pdfExportComponent = useRef(null);

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
    <section id="sub_contents" style={{ width: '100vw', height: '100vh' }}>
      <div className="sub01_wrap">
        <h2 className="h2_tit2">Loading...</h2>
      </div>
      <div className="content clfix">
        {Array.from({ length: 20 }).map((_, i) => (
          <Skeleton key={i} />
        ))}
      </div>
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
        <section
          id="sub_contents"
          ref={pdfExportComponent}
          style={{
            fontFamily: "'Noto Sans KR'",
          }}
        >
          <PdfExportButton exportTarget={pdfExportComponent} />
          <Box className="sub01_wrap">
            <Grid container spacing={1} direction="column">
              <Grid item>
                <Typography variant="h2">
                  Risk Report{' '}
                  <em style={{ fontSize: '0.5em' }}>
                    {new Intl.DateTimeFormat('ko-KR', {
                      dateStyle: 'full',
                    }).format(new Date())}{' '}
                    (24h)
                  </em>
                </Typography>
              </Grid>
              <Grid item>
                <Typography>{getLineBreakText(data.overview)}</Typography>
              </Grid>
            </Grid>

            <Grid container spacing={1} mt={3} direction="column">
              <Grid item>
                <Typography variant="h3">리스크 브리핑</Typography>
              </Grid>
              <Grid item>
                <ExclusiveSelect
                  selectOptions={['1d', '1wk', '1m', '1yr', 'all']}
                  selectedValue={dateRange}
                  setSelectedValue={setDateRange}
                  selectHandler={selectHandler}
                />
              </Grid>

              <Grid
                item
                container
                spacing={5}
                mt={1}
                direction="row"
                justifyContent="space-between"
                alignItems="flex-start"
              >
                <Grid item xs={12} md={6}>
                  <Graphs />
                </Grid>
                <Grid item xs={12} md={6}>
                  <Grid container direction="column" spacing={3}>
                    {data.briefingContents.map((props) => {
                      return <ScrappedArticle {...props} />;
                    })}
                  </Grid>
                </Grid>
              </Grid>
            </Grid>

            <div className="content clfix">
              <h2>중대 위협</h2>
              <Grid
                container
                direction="row"
                justifyContent="space-evenly"
                alignItems="center"
                sx={{ mt: '1rem' }}
              >
                {data.majorEvents.map(
                  ({
                    imageUrl,
                    title,
                    threatType,
                    sourceName,
                    url,
                    datetime,
                  }) => (
                    <ThreatMediaCard
                      imageUrl={imageUrl}
                      title={title}
                      threatType={threatType}
                      sourceChannel={sourceName}
                      sourceTime={datetime}
                      href={url}
                    />
                  )
                )}
              </Grid>
            </div>
          </Box>
        </section>
      )}
    </>
  );
};

export default RiskReport;
