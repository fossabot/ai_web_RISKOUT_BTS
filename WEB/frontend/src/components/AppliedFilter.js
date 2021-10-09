import { Chip, Grid } from '@mui/material';

export default function AppliedFilter({ appliedFilters, setAppliedFilters }) {
  const handleDelete = (filterToDelete) => () => {
    alert(filterToDelete);
    setAppliedFilters((filters) =>
      filters.filter((filter) => filter !== filterToDelete)
    );
  };
  return (
    <Grid
      sx={{
        display: 'flex',
        justifyContent: 'start',
        flexWrap: 'wrap',
        listStyle: 'none',
        m: 0,
      }}
    >
      {appliedFilters.map((data, id) => (
        <Chip
          key={id}
          color="primary"
          label={data}
          onDelete={handleDelete(data)}
        />
      ))}
    </Grid>
  );
}
