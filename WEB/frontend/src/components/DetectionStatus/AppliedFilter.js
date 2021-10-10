import { Chip, Grid } from '@mui/material';

import { useRecoilState } from 'recoil';
import { filterListState } from '../../atoms/filterListState';

export default function AppliedFilter() {
  const [filterList, setFilterList] = useRecoilState(filterListState);

  const handleDelete = (filterToDelete) => () => {
    setFilterList(filterList.filter((filter) => filter !== filterToDelete));
  };

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
      {filterList.map((data, id) => (
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
