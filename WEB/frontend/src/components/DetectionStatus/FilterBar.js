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
import CachedIcon from '@mui/icons-material/Cached';
import FilterCheckbox from './FilterCheckbox';

export default function FilterBar({ search, filter, toggleFilter }) {
  return (
    <Card
      sx={{ right: 0, marginTop: '38px', minHeight: '100%' }}
      elevation={1}
      spacing={3}
    >
      <CardHeader
        action={
          <Button
            style={{ fontSize: '10px', marginTop: '10px' }}
            // endIcon={<CachedIcon />}
            size="small"
          >
            RESET
          </Button>
        }
        titleTypographyProps={{ variant: 'body1' }}
        title="FILTER"
      />
      <Divider />

      {[
        ['단체', 'ORG'],
        ['인물', 'CVL'],
        ['시간대', 'TIM'],
      ].map(([filterLabel, filterCode]) => {
        const filterTags = Object.entries(search.filterTags[filterCode]);
        return (
          <CardContent style={{ marginBottom: '16px' }}>
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
                      onToggle={toggleFilter}
                      checked={filter.includes(hashtag)}
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
