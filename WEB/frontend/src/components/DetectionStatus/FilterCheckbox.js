import { Grid, Stack } from '@mui/material';
import { Box } from '@mui/system';

export default function filterCheckbox(props) {
  const { count, hashtag, checked, onToggle } = props;
  const onChange = (e) => {
    onToggle(hashtag);
  };
  return (
    <Stack direction="row" alignItems="center" justifyContent="space-between">
      <Stack direction="row" justifyContent="space-between" spacing={0.5}>
        <input type="checkbox" onChange={onChange} checked={checked} />
        <p>{hashtag}</p>
      </Stack>
      <em>{count > 10 ? '10+' : count}</em>
    </Stack>
  );
}
