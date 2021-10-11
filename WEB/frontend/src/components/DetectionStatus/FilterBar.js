import {
  Box,
  Button,
  Card,
  CardHeader,
  CardContent,
  Divider,
  Stack,
  Typography,
} from '@mui/material';
import FilterCheckbox from './FilterCheckbox';

import { useRecoilState, useRecoilValue } from 'recoil';
import { filterListState } from '../../atoms/filterListState';
import { searchListState } from '../../atoms/searchListState';

export default function FilterBar() {
  const filterList = useRecoilValue(filterListState);
  const searchList = useRecoilValue(searchListState);

  return (
    <Card
      sx={{ right: 0, marginTop: '38px', minHeight: '100%' }}
      elevation={1}
      spacing={3}
    >
      <CardHeader
        action={
          <Button style={{ fontSize: '10px', marginTop: '10px' }} size="small">
            RESET
          </Button>
        }
        titleTypographyProps={{ variant: 'body1', fontSize: '1.5rem', fontFamily: "Noto sans KR", fontWeight: 600 }}
        title="FILTER"
      />
      <Divider />

      {Object.entries(namedEntityMap).map(([filterLabel, filterCode]) => {
        const filterTags = Object.entries(searchList.filterTags[filterCode]);
        return (
          <CardContent style={{ marginBottom: '16px', fontFamily: "Noto sans KR" }}>
            <Box className="filter_con">
              <Stack
                direction="row"
                alignItems="center"
                justifyContent="space-between"
              >
                <Typography>글에서 찾은 {filterLabel}</Typography>
                <Typography>{filterTags.length}</Typography>
              </Stack>
              <Box>
                {/* <FilterCheckbox count={10} hashtag="myHashtag" key="myHashtag" onToggle={toggleFilter} /> */}
                {filterTags
                  .sort(([_, a], [__, b]) => (a < b ? 1 : -1))
                  .map(([hashtag, freq], i) => (
                    <FilterCheckbox
                      count={freq}
                      hashtag={hashtag}
                      key={hashtag}
                      checked={filterList.includes(hashtag)}
                    />
                  ))}
                <Button
                  size="small"
                  sx={{ float: 'right', marginRight: '-15px' }}
                >
                  더보기
                </Button>
              </Box>
            </Box>
          </CardContent>
        );
      })}
    </Card>
  );
}

const namedEntityMap = { 단체: 'ORG', 인물: 'CVL', 시간대: 'TIM' };
