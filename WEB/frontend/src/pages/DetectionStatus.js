import { useState, useEffect } from 'react';
import { useSnackbar } from 'notistack';
import axios from 'axios';
import {
  Box,
  Container,
  Grid,
  Paper,
  Typography,
  Divider,
} from '@mui/material';

import AppliedFilters from '../components/DetectionStatus/AppliedFilter';
import DetectionTable from '../components/DetectionStatus/DetectionTable';
import FilterBar from '../components/DetectionStatus/FilterBar';
import Search from '../components/Search';
import SecretsDetailModal from '../components/Modal/SecretsDetailModal';
import { useSessionStorage } from '../js/util';

export default function DetectionStatus() {
  const [isDetailModalOpen, setDetailModalOpen] = useState(false);
  const [detailModalData, setDetailModalData] = useState({
    id: 0,
    created_at: '',
    site_url: '',
    thumbnail_url: '',
    category: '',
    title: '',
    contentBody: '',
    summarized: '',
    positivity: 0,
    entities: {},
  });
  const [appliedFilters, setAppliedFilters] = useState([
    'GP/GOP',
    '정체단',
    '사이버작전센터',
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
  const { enqueueSnackbar } = useSnackbar();

  const toggleFilter = (hashtag) => {
    if (appliedFilters.includes(hashtag)) {
      setAppliedFilters(appliedFilters.filter((val) => val !== hashtag));
    } else {
      appliedFilters.push(hashtag);
      setAppliedFilters([...appliedFilters]);
    }
  };

  const handleDelete = (filterToDelete) => () => {
    alert(filterToDelete);
    setAppliedFilters((filters) =>
      filters.filter((filter) => filter !== filterToDelete)
    );
  };

  // => search
  useEffect(() => {
    const searchUrl = `/static/SecretData.example.json`;
    async function fetchSearch() {
      axios.get(searchUrl).then((data) => {
        setSearchResults(data.data);
      });
    }
    fetchSearch();
  }, [appliedFilters]);

  const showDetailModal = (id) => {
    const data = searchResults.contents.filter((x) => x.id == id).pop(0); // popping doesn't affect original array
    console.log(
      data,
      searchResults.contents.filter((x) => x.id == id),
      searchResults
    );
    setDetailModalData(data);
    setDetailModalOpen(true);
  };

  const [getCart, addCart] = useSessionStorage('riskoutShoppingCart');
  const scrapArticle = (id) => {
    addCart(id);
    const article = searchResults.contents.filter((x) => x.id == id).pop();
    enqueueSnackbar('Scrapped article | ' + article.title, {
      variant: 'success',
      autoHideDuration: 10000,
    });
  };

  const analyzePage = (id) => {
    console.log('TODO: analyzePage article ', id);
    alert('TODO: analyzePage article ' + id);
  };

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} md={10} container spacing={3} direction="column">
        <Grid width="100%" item>
          <Typography mt={1} variant="h5" sx={{ fontWeight: 'bold' }}>
            탐지 현황
          </Typography>
          <Search />
          <Typography mt={3} color="primary">
            {searchResults.contentsLength}개 결과 | {appliedFilters.length}개
            필터 적용중
          </Typography>
        </Grid>
        <Grid width="100%" item justify="center">
          <AppliedFilters
            appliedFilters={appliedFilters}
            handleDelete={handleDelete}
          />
        </Grid>
        <Grid item justify="center">
          <DetectionTable
            data={searchResults}
            showDetailModal={showDetailModal}
            scrapArticle={scrapArticle}
          />
        </Grid>
      </Grid>
      <Grid item xs={0} md={2} display={{ xs: 'none', md: 'block' }}>
        <FilterBar
          search={searchResults}
          filter={appliedFilters}
          toggleFilter={toggleFilter}
        />
      </Grid>
      <SecretsDetailModal
        isOpen={isDetailModalOpen}
        setOpen={setDetailModalOpen}
        scrapArticle={scrapArticle}
        data={detailModalData}
      />
    </Grid>
  );
}
