import {
  Chip,
  Stack,
  Link,
  Grid,
  Typography,
  Card,
  CardMedia,
  CardContent,
} from '@mui/material';

export default function ThreatMediaCard(props) {
  return (
    <Card variant="outlined" sx="width: 400px">
      <CardMedia
        component="img"
        height="150"
        image="https://via.placeholder.com/400x150/09f/fff.png"
      />
      <CardContent>
        <Typography
          variant="h3"
          sx={{
            mt: '1em',
            mb: '1em',
            lineHeight: '1.67',
            display: '-webkit-box',
            WebkitLineClamp: '2',
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            WebkitBoxOrient: 'vertical',
            // -webkit-box-orient: vertical;
          }}
        >
          문재인: 이명박, 박근혜가 5.18 민주화운동 기념식에 참석하지 않았다고
          주장
        </Typography>
        <Grid
          container
          direction="row"
          justifyContent="space-between"
          alignItems="center"
          sx={{ mt: '1rem' }}
        >
          <Stack direction="row" spacing={1}>
            <Chip
              label="허위뉴스"
              // variant="outlined"
              color="error"
              size="medium"
              sx={{ height: '2.4rem', fontSize: '1rem' }}
            />
          </Stack>
          <Link href="#" target="_blank" rel="noopener" underline="hover">
            연합뉴스 2021-10-03 10:33PM
          </Link>
        </Grid>
      </CardContent>
    </Card>
  );
}
