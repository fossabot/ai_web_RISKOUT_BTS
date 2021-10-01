import SentimentBar from '../components/Dashboard/SentimentBar';
import SentimentPie from '../components/Dashboard/SentimentPie';
import ArticleVolumeBar from '../components/Dashboard/ArticleVolumeBar';
import GeoEventPlot from '../components/Dashboard/GeoEventPlot';
import WordCloud from '../components/Dashboard/WordCloud';

import { Container, Box, Grid } from '@mui/material';

import { volumeDummy } from '../dummy/volumeDummy';
import { barDummy } from '../dummy/barDummy';
import { pieDummy } from '../dummy/pieDummy';
import { geoDummy } from '../dummy/geoDummy';
import { words } from '../dummy/words';

const options = {
  colors: ['#AEE1E1', '#D3E0DC', '#ECE2E1', '#FCD1D1'],
  enableTooltip: true,
  deterministic: true,
  fontFamily: 'impact',
  fontSizes: [5, 60],
  fontStyle: 'normal',
  fontWeight: 'normal',
  padding: 1,
  rotations: 3,
  rotationAngles: [-30, 30],
  scale: 'linear',
  spiral: 'rectangular',
  transitionDuration: 1000,
};

export default function Dashboard() {
  return (
    <Box
      m={3}
      sx={{
        backgroundColor: 'background.default',
        minHeight: '100%',
        py: 3,
      }}
    >
      <Container maxWidth={false}>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={12} md={12} lg={12}>
            <h2>개요</h2>
          </Grid>
          <Grid item xs={12} sm={12} md={12} lg={8}>
            <WordCloud options={options} words={words} />
          </Grid>
          <Grid item xs={12} sm={12} md={12} lg={4}>
            <ArticleVolumeBar data={volumeDummy} />
          </Grid>
          <Grid item xs={12} sm={12} md={12} lg={4}>
            <SentimentBar data={barDummy} />
          </Grid>
          <Grid item xs={12} sm={12} md={12} lg={3}>
            <SentimentPie data={pieDummy} />
          </Grid>
          <Grid item xs={12} sm={12} md={12} lg={5}>
            <GeoEventPlot data={geoDummy} />
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}
