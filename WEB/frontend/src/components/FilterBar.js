import {
  Box,
  Button,
  Card,
  CardHeader,
  CardContent,
  Divider,
} from '@mui/material';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';

import FilterCheckbox from '../components/FilterCheckbox';

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
                <h5>글에서 찾은 {filterLabel}</h5>
                <span>{filterTags.length}</span>
                <ul className="keyword">
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
                </ul>
                <button className="more_btn">더보기</button>
              </div>
            );
          })}
        </Box>
      </CardContent>
    </Card>
  );
}
