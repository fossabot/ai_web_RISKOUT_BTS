import { useEffect } from 'react';
import { ResponsiveLine } from '@nivo/line';
import {
  Card,
  CardHeader,
  CardContent,
  Box,
  Button,
  Divider,
} from '@mui/material';
import useFetch from '../../hooks/useFetch';

const ArticleVolumeLine = () => {
  const { data, error, isPending } = useFetch(
    `https://playff-osamhack2021-ai-web-riskout-bts-45v7rgwx3j4vq-8000.githubpreview.dev/article-volume`
  );

  useEffect(() => {
    console.log(data);
  }, [data]);

  return (
    <Card style={{ height: '400px' }}>
      <CardHeader title="기사 변화량" />
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
          {data && (
            <ResponsiveLine
              data={data}
              margin={{ top: 10, right: 110, bottom: 50, left: 60 }}
              xScale={{ type: 'point' }}
              yScale={{
                type: 'linear',
                min: 'auto',
                max: 'auto',
                stacked: false,
                reverse: false,
              }}
              curve="monotoneX"
              axisTop={null}
              axisRight={null}
              axisBottom={{
                orient: 'bottom',
                tickSize: 5,
                tickPadding: 5,
                tickRotation: 0,
                legend: '기사 변화량',
                legendOffset: 36,
                legendPosition: 'middle',
              }}
              axisLeft={{
                orient: 'left',
                tickSize: 5,
                tickPadding: 5,
                tickRotation: 0,
                legend: 'volume',
                legendOffset: -40,
                legendPosition: 'middle',
              }}
              colors={{ scheme: 'nivo' }}
              pointSize={10}
              pointColor={{ theme: 'background' }}
              pointBorderWidth={2}
              pointBorderColor={{ from: 'serieColor' }}
              pointLabelYOffset={-12}
              useMesh={true}
              legends={[
                {
                  anchor: 'bottom-right',
                  direction: 'column',
                  justify: false,
                  translateX: 100,
                  translateY: 0,
                  itemsSpacing: 0,
                  itemDirection: 'left-to-right',
                  itemWidth: 80,
                  itemHeight: 20,
                  itemOpacity: 0.75,
                  symbolSize: 12,
                  symbolShape: 'circle',
                  symbolBorderColor: 'rgba(0, 0, 0, .5)',
                  effects: [
                    {
                      on: 'hover',
                      style: {
                        itemBackground: 'rgba(0, 0, 0, .03)',
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

export default ArticleVolumeLine;
