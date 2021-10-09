import { useState, useEffect } from 'react';
import axios from 'axios';
import { Box, Grid, Paper, Typography, Divider } from '@mui/material';

import SearchBar from 'material-ui-search-bar';
import { styled } from '@mui/material/styles';

import AppliedFilters from '../components/AppliedFilter';
import DetectionTable from '../components/DetectionTable';
import FilterBar from '../components/FilterBar';

export default function DetectionStatus() {
  const [appliedFilters, setAppliedFilters] = useState([
    '전투시행세부규칙: 군사기밀',
    'GP/GOP: 군사기밀',
    '계룡대: 장소',
    '사이버작전센터: 조직',
  ]);
  const [searchResults, setSearchResults] = useState({
    contentsLength: 0,
    contents: [],
    filterTags: {
      ORG: {},
      CVL: {},
      TIM: {},
    },
  });

  const toggleFilter = (hashtag) => {
    if (appliedFilters.includes(hashtag)) {
      setAppliedFilters(appliedFilters.filter((val) => val !== hashtag));
    } else {
      appliedFilters.push(hashtag);
      setAppliedFilters([...appliedFilters]);
    }
  };

  //TODO: hooks 따로 뺄 것
  useEffect(() => {
    const searchUrl = `/dummy/searchData.json`;
    async function fetchSearch() {
      axios.get(searchUrl).then((data) => {
        setSearchResults(data.data.search);
      });
    }
    fetchSearch();
  }, []);

  return (
    <Box
      m={2}
      sx={{
        backgroundColor: 'inherit',
        minHeight: '100%',
        py: 0,
      }}
    >
      <Grid container spacing={3}>
        <Grid item xs={9} container spacing={3} direction="column">
          <Grid width="100%" item>
            <Typography mb={2} variant="h6">
              탐지 현황
            </Typography>
            <SearchBar />
            <Typography mt={3} color="primary">
              {searchResults.contentsLength}개 결과 | {appliedFilters.length}개
              필터 적용중
            </Typography>
          </Grid>
          <Grid width="100%" item justify="center">
            <AppliedFilters
              appliedFilters={appliedFilters}
              setAppliedFilters={setAppliedFilters}
            />
          </Grid>
          <Grid item justify="center">
            <DetectionTable data={searchResults} />
          </Grid>
        </Grid>
        <Grid item xs={3} mt={6}>
          <FilterBar
            search={searchResults}
            filter={appliedFilters}
            toggleFilter={toggleFilter}
          />
        </Grid>
      </Grid>
    </Box>
  );
}
