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
  // colors 를 바꾸면 전체 Theme 이 바뀝니다.
  colors: ['#EEEEEE', '#686D76', '#373A40', '#00ADB5'],
  enableTooltip: true,
  deterministic: true,
  fontFamily: 'impact',
  fontSizes: [5, 60],
  fontStyle: 'normal',
  fontWeight: 'normal',
  padding: 1,
  rotations: 3,
  rotationAngles: [-30, 30],
  scale: 'sqrt',
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
          <Grid item xs={12} sm={12} md={12} lg={5}>
            <WordCloud options={options} words={words} />
          </Grid>
          <Grid item xs={12} sm={12} md={12} lg={4}>
            <ArticleVolumeBar data={volumeDummy} colors={options.colors} />
          </Grid>
          <Grid item xs={12} sm={12} md={12} lg={3}>
            <ArticleVolumeBar data={volumeDummy} colors={options.colors} />
          </Grid>
          <Grid item xs={12} sm={12} md={12} lg={4}>
            <SentimentBar data={barDummy} colors={options.colors} />
          </Grid>
          <Grid item xs={12} sm={12} md={12} lg={3}>
            <SentimentPie data={pieDummy} colors={options.colors} />
          </Grid>
          <Grid item xs={12} sm={12} md={12} lg={5}>
            <GeoEventPlot data={geoDummy} colors={options.colors} />
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}
