import {
  Box,
  Button,
  Card,
  CardHeader,
  CardContent,
  Divider,
  Stack,
} from '@mui/material';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';

import FilterCheckbox from './FilterCheckbox';

export default function FilterBar({ search, filter, toggleFilter }) {
  return (
    <Card sx={{ height: '100vh', right: 0 }} elevation={5}>
      <CardHeader
        action={
          <Button
            style={{ fontSize: '10px', marginTop: '10px' }}
            endIcon={<ArrowDownwardIcon />}
            size="small"
          >
            RESET
          </Button>
        }
        titleTypographyProps={{ variant: 'body1' }}
        title="FILTER"
      />
      <CardContent>
        <Box
          sx={{
            height: 400,
            position: 'relative',
          }}
        >
          {[
            ['단체', 'ORG'],
            ['인물', 'CVL'],
            ['시간대', 'TIM'],
          ].map(([filterLabel, filterCode]) => {
            const filterTags = Object.entries(search.filterTags[filterCode]);
            return (
              <div className="filter_con">
                <Stack
                  direction="row"
                  alignItems="center"
                  justifyContent="space-between"
                >
                  <h5>글에서 찾은 {filterLabel}</h5>
                  <span>{filterTags.length}</span>
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
                        onToggle={toggleFilter}
                        checked={filter.includes(hashtag)}
                      />
                    ))}
                </Box>
                <button className="more_btn">더보기</button>
              </div>
            );
          })}
        </Box>
      </CardContent>
    </Card>
  );
}
