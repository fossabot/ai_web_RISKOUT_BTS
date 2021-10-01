import ReactWordcloud from 'react-wordcloud';
import {
  Card,
  CardHeader,
  CardContent,
  Box,
  Button,
  Divider,
} from '@mui/material';
import { ArrowDropDown } from '@mui/icons-material';

import 'tippy.js/dist/tippy.css';
import 'tippy.js/animations/scale.css';

const WordCloud = ({ options, words }) => {
  return (
    <Card style={{ height: '400px' }}>
      <CardHeader title="여론 현황 (언급 횟수)" />
      <Divider />
      <CardContent>
        <Box
          sx={{
            height: 300,
            position: 'relative',
          }}
        >
          <ReactWordcloud options={options} words={words} />
        </Box>
      </CardContent>
    </Card>
  );
};

export default WordCloud;
