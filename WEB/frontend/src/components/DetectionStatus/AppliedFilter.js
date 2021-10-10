import { Chip, Grid } from '@mui/material';

export default function AppliedFilter({ appliedFilters, handleDelete }) {
  return (
    <Grid
      container
      sx={{
        display: 'flex',
        justifyContent: 'start',
        flexWrap: 'wrap',
        listStyle: 'none',
        m: 0,
      }}
      spacing={1}
    >
      {appliedFilters.map((data, id) => (
        <Grid item>
          <Chip
            key={id}
            sx={{ borderRadius: '5px' }}
            label={data}
            onDelete={handleDelete(data)}
          />
        </Grid>
      ))}
    </Grid>
  );
}
