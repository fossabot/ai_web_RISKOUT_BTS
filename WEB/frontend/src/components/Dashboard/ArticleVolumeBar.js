import { ResponsiveBar } from '@nivo/bar';
import {
  Card,
  CardHeader,
  CardContent,
  Box,
  Button,
  Divider,
} from '@mui/material';
import useFetch from '../../hooks/useFetch';

const ArticleVolumeBar = ({ colors }) => {
  const { data, error, isPending } = useFetch(`/article-volume`);

  return (
    <Card style={{ height: '400px' }}>
      <CardHeader title="기사 변화량" />
      <Divider />
      <CardContent>
        <Box
          sx={{
            height: 350,
            position: 'relative',
          }}
        >
          {error && <div>{error} </div>}
          {isPending && <div>Loading...</div>}
          {data && (
            <ResponsiveBar
              data={data}
              keys={['Real News', 'Fake News']}
              indexBy="date"
              margin={{ top: 0, right: 130, bottom: 100, left: 60 }}
              padding={0.3}
              groupMode="grouped"
              valueScale={{ type: 'linear' }}
              indexScale={{ type: 'band', round: true }}
              valueFormat={{ format: '', enabled: false }}
              colors={colors}
              borderColor={{ from: 'color', modifiers: [['darker', 1.6]] }}
              axisTop={null}
              axisRight={null}
              axisBottom={{
                tickSize: 5,
                tickPadding: 5,
                tickRotation: 0,
                legendPosition: 'middle',
                legendOffset: 32,
              }}
              axisLeft={{
                tickSize: 5,
                tickPadding: 5,
                tickRotation: 0,
                legend: 'volumes',
                legendPosition: 'middle',
                legendOffset: -40,
              }}
              labelSkipWidth={12}
              labelSkipHeight={12}
              labelTextColor={{ from: 'color', modifiers: [['darker', 1.6]] }}
              legends={[
                {
                  dataFrom: 'keys',
                  anchor: 'bottom-right',
                  direction: 'column',
                  justify: false,
                  translateX: 120,
                  translateY: 0,
                  itemsSpacing: 2,
                  itemWidth: 100,
                  itemHeight: 20,
                  itemDirection: 'left-to-right',
                  itemOpacity: 0.85,
                  symbolSize: 20,
                  effects: [
                    {
                      on: 'hover',
                      style: {
                        itemOpacity: 1,
                      },
                    },
                  ],
                },
              ]}
            />
          )}
        </Box>
      </CardContent>
    </Card>
  );
};

export default ArticleVolumeBar;