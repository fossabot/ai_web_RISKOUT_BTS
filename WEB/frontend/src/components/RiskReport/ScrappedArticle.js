import { getLineBreakText } from '../../js/util';
import { Chip, Stack, Link, Grid } from '@mui/material';

export default function ScrappedArticle({
  url,
  title,
  summary,
  characteristics,
  sourceName,
  datetime,
}) {
  return (
    <Grid item width="100%" component="article">
      <Link href={url} target="_blank" rel="noopener" underline="hover">
        <h3>{title}</h3>
      </Link>
      {getLineBreakText(summary)}
      <Grid
        container
        direction="row"
        justifyContent="space-between"
        alignItems="center"
        sx={{ mt: '1rem' }}
      >
        <Stack direction="row" spacing={1}>
          {characteristics.map((c) => (
            <Chip
              label={c}
              variant="outlined"
              size="medium"
              sx={{ height: '2.4rem', fontSize: '1rem' }}
            />
          ))}
        </Stack>
        <Link href={url} target="_blank" rel="noopener" underline="hover">
          <em>원본:</em> {sourceName} {datetime}
        </Link>
      </Grid>
    </Grid>
  );
}
