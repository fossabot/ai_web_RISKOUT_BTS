import ReactWordcloud from 'react-wordcloud';
import {
  Card,
  CardHeader,
  CardContent,
  Box,
  Button,
  Divider,
} from '@mui/material';
import useFetch from '../../hooks/useFetch';

import 'tippy.js/dist/tippy.css';
import 'tippy.js/animations/scale.css';

const WordCloud = ({ options }) => {
  const { data, error, isPending } = useFetch(
    `https://playff-osamhack2021-ai-web-riskout-bts-45v7rgwx3j4vq-8000.githubpreview.dev/wordcloud`
  );

  return (
    <Card style={{ height: '400px' }}>
      <CardHeader title="오늘의 키워드" />
      <Divider />
      <CardContent>
        <Box
          sx={{
            height: 300,
            position: 'relative',
          }}
        >
          {error && <div>{error} </div>}
          {isPending && <div>Loading...</div>}
          {data && <ReactWordcloud options={options} words={data} />}
        </Box>
      </CardContent>
    </Card>
  );
};

export default WordCloud;
