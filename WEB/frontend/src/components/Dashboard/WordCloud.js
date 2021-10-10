import ReactWordcloud from 'react-wordcloud';
import {
  Card,
  CardHeader,
  CardContent,
  Box,
  LinearProgress,
  Divider,
} from '@mui/material';
import useFetch from '../../hooks/useFetch';
import { getWordCloud } from '../../lib/api/dashboard/getWordCloud';

import 'tippy.js/dist/tippy.css';
import 'tippy.js/animations/scale.css';

const WordCloud = ({ options }) => {
  const { data } = getWordCloud();

  return (
    <Card style={{ height: '400px' }}>
      <CardHeader title="오늘의 키워드" />
      <Divider />
      {data ? (
        <CardContent>
          <Box
            sx={{
              height: 300,
              position: 'relative',
            }}
          >
            <ReactWordcloud options={options} words={data} />
          </Box>
        </CardContent>
      ) : (
        <Box sx={{ width: '100%', color: 'grey.500' }}>
          <LinearProgress color="inherit" />
        </Box>
      )}
    </Card>
  );
};

export default WordCloud;
