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
  const {
    imageUrl,
    title,
    threatType,
    sourceChannel,
    sourceTime,
    href,
  } = props;

  const imgWidth = 300;
  const imgHeight = 150;
  return (
    <Card variant="outlined" sx={`width: ${imgWidth}px`}>
      <a href={href} style={{ padding: 0, margin: 0 }}>
        <CardMedia
          component="img"
          height={`${imgHeight}`}
          image={imageUrl}
          sx={{ height: `${imgHeight}px`, width: `${imgWidth}px` }}
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
            {title}
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
                label={threatType}
                // variant="outlined"
                color="error"
                size="medium"
                sx={{ height: '2.4rem', fontSize: '1rem' }}
              />
            </Stack>
            <Link href={href} target="_blank" rel="noopener" underline="hover">
              {sourceChannel} {sourceTime}
            </Link>
          </Grid>
        </CardContent>
      </a>
    </Card>
  );
}
